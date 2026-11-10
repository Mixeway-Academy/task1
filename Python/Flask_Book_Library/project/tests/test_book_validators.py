import unittest
from datetime import date

from loader import load

validators = load('project.books.validators')
ValidationError = validators.ValidationError


class ValidatorTestCase(unittest.TestCase):
    """Helpers: every case is reported separately via subTest."""

    def assert_valid(self, validator, cases):
        """cases: iterable of (input, expected_output)."""
        for value, expected in cases:
            with self.subTest(value=value):
                self.assertEqual(validator(value), expected)

    def assert_invalid(self, validator, values):
        for value in values:
            with self.subTest(value=value):
                with self.assertRaises(ValidationError):
                    validator(value)


class NameValidatorTests(ValidatorTestCase):
    def test_valid_names_are_accepted_unchanged(self):
        names = [
            "Harry Potter & the Philosopher's Stone",
            "C++ Primer",
            "Catch-22",
            "1984",
            "Zbrodnia i kara",
            "Mistrz i Małgorzata",
            "Dziady (część III)",
            "Dune: Messiah",
            "What If?",
        ]
        self.assert_valid(validators.validate_name, [(n, n) for n in names])

    def test_whitespace_is_trimmed_and_collapsed(self):
        self.assert_valid(validators.validate_name, [("  Pan \t Tadeusz\n ", "Pan Tadeusz")])

    def test_xss_payloads_are_rejected(self):
        self.assert_invalid(validators.validate_name, [
            "<script>alert(1)</script>",
            "<img src=x onerror=alert(1)>",
            "<svg/onload=alert(1)>",
            '" onmouseover="alert(1)',
            "&lt;script&gt;alert(1)",
            "{{7*7}}",
        ])

    def test_malformed_input_is_rejected(self):
        self.assert_invalid(validators.validate_name, [
            None, "", "   ", 123, ["x"], "!!!", "name\x00", "A" * 65,
        ])

    def test_maximum_length_is_accepted(self):
        self.assertEqual(validators.validate_name("A" * 64), "A" * 64)


class AuthorValidatorTests(ValidatorTestCase):
    def test_valid_authors_are_accepted(self):
        authors = ["J.R.R. Tolkien", "Bolesław Prus", "O'Brien", "Jean-Paul Sartre"]
        self.assert_valid(validators.validate_author, [(a, a) for a in authors])

    def test_invalid_authors_are_rejected(self):
        self.assert_invalid(validators.validate_author, [
            "<script>alert(1)</script>", "<b>x</b>", "Author123", "a=b",
            None, "", "   ", 5, "...", "A" * 65,
        ])


class YearValidatorTests(ValidatorTestCase):
    def test_valid_years_are_accepted(self):
        current = date.today().year
        self.assert_valid(validators.validate_year_published, [
            (1999, 1999),
            ("1999", 1999),
            (" 2001 ", 2001),
            (1, 1),
            (current, current),
        ])

    def test_invalid_years_are_rejected(self):
        self.assert_invalid(validators.validate_year_published, [
            date.today().year + 1, 0, -5, "abc", "<script>alert(1)</script>",
            "1999<script>", True, 1999.0, None, "", "12345",
        ])


class ChoiceValidatorTests(ValidatorTestCase):
    def test_valid_book_types_are_accepted(self):
        self.assert_valid(validators.validate_book_type, [
            ("2days", "2days"), ("5days", "5days"), ("10days", "10days"), (" 5days ", "5days"),
        ])

    def test_invalid_book_types_are_rejected(self):
        self.assert_invalid(validators.validate_book_type, [
            "1day", "2DAYS", "<script>alert(1)</script>", "", None, 5,
        ])

    def test_valid_statuses_are_accepted(self):
        self.assert_valid(validators.validate_status, [
            ("available", "available"), ("loaned", "loaned"),
        ])

    def test_invalid_statuses_are_rejected(self):
        self.assert_invalid(validators.validate_status, ["x", "Available", "", None, "<b>"])


class ModuleContractTests(unittest.TestCase):
    def test_validation_error_is_a_value_error(self):
        self.assertTrue(issubclass(ValidationError, ValueError))

    def test_every_book_field_has_a_validator(self):
        self.assertEqual(
            set(validators.BOOK_VALIDATORS),
            {'name', 'author', 'year_published', 'book_type', 'status'},
        )


if __name__ == '__main__':
    unittest.main()