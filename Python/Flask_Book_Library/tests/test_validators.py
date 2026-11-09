"""Validator unit tests (valid and invalid input). Run: python -m unittest discover -s tests -v"""
import os
import unittest

# Use an in-memory DB; must be set before importing the app
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")

from project.books.models import Book  # noqa: E402
from project.customers.models import Customer  # noqa: E402
from project.validators import (  # noqa: E402
    validate_age,
    validate_author,
    validate_book_title,
    validate_book_type,
    validate_city,
    validate_person_name,
    validate_year_published,
)

# Common XSS payloads - all must be rejected
XSS_PAYLOADS = [
    "<script>alert(1)</script>",
    "<img src=x onerror=alert(1)>",
    "\"><svg onload=alert(1)>",
    "<b>bold</b>",
    "Jan<script>",
    "&lt;script&gt;alert(1)&lt;/script&gt;",
    "<iframe src=javascript:alert(1)>",
    "x\" onmouseover=\"alert(1)",
    "{{7*7}}",
    "`alert(1)`",
]


class PersonNameValidatorTest(unittest.TestCase):
    VALID = ["Jan Kowalski", "Zażółć Gęślą", "Anna-Maria O'Neil", "Li", "Łukasz Żółkiewski-Nowak"]
    INVALID = [
        "", "   ", "J", "a" * 65,        # length
        "Jan2", "Jan_Kowalski",          # digits / underscore
        "-Jan", "Jan-", "Jan  Kowalski", # edge hyphen, double space
        "Jan\nKowalski", "Jan\tKowalski",
        "Jan (Kowalski)", "javascript:alert(1)",
        None, 123,
    ]

    def test_valid(self):
        for value in self.VALID:
            with self.subTest(value=value):
                self.assertEqual(validate_person_name(value), value)

    def test_strips_surrounding_whitespace(self):
        self.assertEqual(validate_person_name("  Jan Kowalski  "), "Jan Kowalski")

    def test_invalid(self):
        for value in self.INVALID + XSS_PAYLOADS:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    validate_person_name(value)


class AuthorValidatorTest(unittest.TestCase):
    VALID = ["J.R.R. Tolkien", "Stanisław Lem", "Antoine de Saint-Exupéry", "Martin Luther King Jr."]
    INVALID = ["", "Tolkien (J.R.R.)", "Lem 2", ".Lem", "Lem;", None]

    def test_valid(self):
        for value in self.VALID:
            with self.subTest(value=value):
                self.assertEqual(validate_author(value), value)

    def test_invalid(self):
        for value in self.INVALID + XSS_PAYLOADS:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    validate_author(value)


class CityValidatorTest(unittest.TestCase):
    VALID = ["Warszawa", "Bielsko-Biała", "St. Louis", "Kraków", "L'Aquila"]
    INVALID = ["", "W", "Warszawa1", "Warszawa!", "00-001 Warszawa", None]

    def test_valid(self):
        for value in self.VALID:
            with self.subTest(value=value):
                self.assertEqual(validate_city(value), value)

    def test_invalid(self):
        for value in self.INVALID + XSS_PAYLOADS:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    validate_city(value)


class BookTitleValidatorTest(unittest.TestCase):
    VALID = [
        "Pan Tadeusz",
        "1984",
        "Harry Potter i Kamień Filozoficzny (tom 1)",
        "Ogniem i mieczem, cz. 2: Bitwa!",
        "Who's Afraid of Virginia Woolf?",
        "Q",
    ]
    INVALID = ["", "   ", "x" * 65, "-Tytuł", "C# dla opornych", "Tytuł / podtytuł", "a=b", None, 1984]

    def test_valid(self):
        for value in self.VALID:
            with self.subTest(value=value):
                self.assertEqual(validate_book_title(value), value)

    def test_invalid(self):
        for value in self.INVALID + XSS_PAYLOADS:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    validate_book_title(value)


class NumberAndChoiceValidatorTest(unittest.TestCase):
    def test_year_valid(self):
        self.assertEqual(validate_year_published("1999"), 1999)
        self.assertEqual(validate_year_published(1450), 1450)

    def test_year_invalid(self):
        for value in ["", "abc", "1e3", "-1", "19 99", "<script>", 1000, 3000, True, None, 19.99]:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    validate_year_published(value)

    def test_age_valid(self):
        self.assertEqual(validate_age("30"), 30)
        self.assertEqual(validate_age(120), 120)

    def test_age_invalid(self):
        for value in ["", "0", "121", "-5", "30 lat", "<img>", 0, False, None]:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    validate_age(value)

    def test_book_type(self):
        for value in ["2days", "5days", "10days"]:
            self.assertEqual(validate_book_type(value), value)
        for value in ["1day", "", "<script>alert(1)</script>", None]:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    validate_book_type(value)


class ModelValidationTest(unittest.TestCase):
    """Validation runs when a domain object is created or modified."""

    def test_valid_book_is_created(self):
        book = Book(name="Solaris", author="Stanisław Lem", year_published="1961", book_type="5days")
        self.assertEqual(book.year_published, 1961)

    def test_book_with_xss_is_rejected_on_creation(self):
        with self.assertRaises(ValueError):
            Book(name="<script>alert(1)</script>", author="Lem", year_published=1961, book_type="5days")
        with self.assertRaises(ValueError):
            Book(name="Solaris", author="<img src=x onerror=alert(1)>", year_published=1961, book_type="5days")

    def test_book_with_xss_is_rejected_on_modification(self):
        book = Book(name="Solaris", author="Stanisław Lem", year_published=1961, book_type="5days")
        with self.assertRaises(ValueError):
            book.name = "<svg onload=alert(1)>"
        self.assertEqual(book.name, "Solaris")

    def test_customer_with_xss_is_rejected(self):
        Customer(name="Jan Kowalski", city="Warszawa", age="30")
        with self.assertRaises(ValueError):
            Customer(name="<img src=x onerror=alert(1)>", city="Warszawa", age=30)
        with self.assertRaises(ValueError):
            Customer(name="Jan Kowalski", city="<b>Warszawa</b>", age=30)


if __name__ == "__main__":
    unittest.main()
