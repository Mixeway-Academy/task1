"""
Testy jednostkowe poprawki Stored XSS (/books/, /customers/, /loans/).

Poprawka działa na poziomie backendu: modele Book, Customer i Loan walidują
pola tekstowe przy tworzeniu obiektu i przy każdej zmianie atrybutu
(sqlalchemy.orm.validates). Złośliwy payload jest odrzucany (ValueError /
HTTP 400) i nigdy nie trafia do bazy danych.
"""
import os
import unittest
from datetime import datetime

# Baza w pamięci - musi być ustawiona PRZED importem aplikacji,
# bo modele wywołują db.create_all() już przy imporcie.
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from project import app, db  # noqa: E402
from project.books.models import Book  # noqa: E402
from project.customers.models import Customer  # noqa: E402
from project.loans.models import Loan  # noqa: E402
from project.validators import validate_text  # noqa: E402


XSS_PAYLOADS = [
    '<script>alert("XSS")</script>',
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert(1)>",
    "<svg/onload=alert(1)>",
    '"><script>alert(1)</script>',
    "javascript:alert(1)//<a>",
    "<iframe src=javascript:alert(1)>",
]

VALID_VALUES = ["Pan Tadeusz", "Adam Mickiewicz", "Łódź", "Harry Potter i Kamień Filozoficzny",
                "Pride & Prejudice", "O'Brien", "Ogniem i mieczem (t. 1)", "1984"]


def loan_kwargs(**overrides):
    kwargs = dict(
        customer_name="Jan Kowalski",
        book_name="Pan Tadeusz",
        loan_date=datetime(2024, 1, 1),
        return_date=datetime(2024, 1, 10),
        original_author="Adam Mickiewicz",
        original_year_published=1834,
        original_book_type="2days",
    )
    kwargs.update(overrides)
    return kwargs


# ---------------------------------------------------------------------------
# 1. Funkcja walidująca
# ---------------------------------------------------------------------------
class ValidateTextTest(unittest.TestCase):
    def test_rejects_xss_payloads(self):
        for payload in XSS_PAYLOADS:
            with self.subTest(payload=payload):
                with self.assertRaises(ValueError):
                    validate_text("name", payload)

    def test_rejects_html_special_chars(self):
        for ch in '<>"`/\\={}':
            with self.subTest(char=ch):
                with self.assertRaises(ValueError):
                    validate_text("name", f"abc{ch}def")

    def test_accepts_valid_values(self):
        for value in VALID_VALUES:
            with self.subTest(value=value):
                self.assertEqual(validate_text("name", value), value)

    def test_strips_whitespace(self):
        self.assertEqual(validate_text("name", "  Jan  "), "Jan")

    def test_rejects_empty_too_long_and_non_string(self):
        for bad in ("", "   ", "a" * 65, None, 123):
            with self.subTest(value=bad):
                with self.assertRaises(ValueError):
                    validate_text("name", bad)

    def test_optional_field_allows_empty(self):
        self.assertEqual(validate_text("author", "", required=False), "")
        self.assertEqual(validate_text("author", None, required=False), "")
        with self.assertRaises(ValueError):
            validate_text("author", "<script>", required=False)


# ---------------------------------------------------------------------------
# 2. Walidacja na poziomie modeli (tworzenie i modyfikacja obiektu)
# ---------------------------------------------------------------------------
class DbTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        self.client = app.test_client()
        self.ctx = app.app_context()
        self.ctx.push()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.rollback()
        db.session.remove()
        db.drop_all()
        self.ctx.pop()


class BookModelTest(DbTestCase):
    def test_create_with_xss_in_name_or_author_raises(self):
        for payload in XSS_PAYLOADS:
            with self.subTest(field="name", payload=payload):
                with self.assertRaises(ValueError):
                    Book(payload, "Autor", 2020, "2days")
            with self.subTest(field="author", payload=payload):
                with self.assertRaises(ValueError):
                    Book("Tytuł", payload, 2020, "2days")

    def test_invalid_book_type_raises(self):
        with self.assertRaises(ValueError):
            Book("Tytuł", "Autor", 2020, "<script>")

    def test_modify_existing_book_with_xss_raises(self):
        book = Book("Pan Tadeusz", "Adam Mickiewicz", 1834, "5days")
        db.session.add(book)
        db.session.commit()
        with self.assertRaises(ValueError):
            book.name = XSS_PAYLOADS[0]
        with self.assertRaises(ValueError):
            book.author = XSS_PAYLOADS[2]
        db.session.rollback()
        self.assertEqual(Book.query.one().name, "Pan Tadeusz")

    def test_valid_book_is_saved(self):
        db.session.add(Book("Pan Tadeusz", "", 1834, "5days"))
        db.session.commit()
        self.assertEqual(Book.query.count(), 1)


class CustomerModelTest(DbTestCase):
    def test_create_with_xss_in_name_or_city_raises(self):
        for payload in XSS_PAYLOADS:
            with self.subTest(field="name", payload=payload):
                with self.assertRaises(ValueError):
                    Customer(payload, "Kraków", 30)
            with self.subTest(field="city", payload=payload):
                with self.assertRaises(ValueError):
                    Customer("Jan Kowalski", payload, 30)

    def test_modify_existing_customer_with_xss_raises(self):
        customer = Customer("Jan Kowalski", "Kraków", 30)
        db.session.add(customer)
        db.session.commit()
        with self.assertRaises(ValueError):
            customer.city = XSS_PAYLOADS[0]

    def test_valid_customer_is_saved(self):
        db.session.add(Customer("Zażółć Gęślą", "Łódź", 30))
        db.session.commit()
        self.assertEqual(Customer.query.count(), 1)


class LoanModelTest(DbTestCase):
    def test_create_with_xss_raises(self):
        for field in ("customer_name", "book_name", "original_author"):
            for payload in XSS_PAYLOADS:
                with self.subTest(field=field, payload=payload):
                    with self.assertRaises(ValueError):
                        Loan(**loan_kwargs(**{field: payload}))

    def test_invalid_book_type_raises(self):
        with self.assertRaises(ValueError):
            Loan(**loan_kwargs(original_book_type="<b>x</b>"))

    def test_valid_loan_is_saved(self):
        db.session.add(Loan(**loan_kwargs()))
        db.session.commit()
        self.assertEqual(Loan.query.count(), 1)


# ---------------------------------------------------------------------------
# 3. Endpointy - payload odrzucony (400) i nic nie trafia do bazy
# ---------------------------------------------------------------------------
class EndpointsTest(DbTestCase):
    def test_books_create_rejects_xss(self):
        resp = self.client.post("/books/create", json={
            "name": XSS_PAYLOADS[0], "author": "Autor",
            "year_published": 2020, "book_type": "2days"})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(Book.query.count(), 0)
        self.assertNotIn("<script>", self.client.get("/books/").get_data(as_text=True))

    def test_books_edit_rejects_xss(self):
        db.session.add(Book("Pan Tadeusz", "Adam Mickiewicz", 1834, "5days"))
        db.session.commit()
        book_id = Book.query.one().id
        resp = self.client.post(f"/books/{book_id}/edit", json={"author": XSS_PAYLOADS[2]})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(Book.query.one().author, "Adam Mickiewicz")

    def test_books_create_accepts_valid(self):
        resp = self.client.post("/books/create", json={
            "name": "Pan Tadeusz", "author": "Adam Mickiewicz",
            "year_published": 1834, "book_type": "5days"})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Book.query.count(), 1)

    def test_customers_create_rejects_xss(self):
        resp = self.client.post("/customers/create", data={
            "name": XSS_PAYLOADS[0], "city": "Kraków", "age": 30})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(Customer.query.count(), 0)
        self.assertNotIn("<script>", self.client.get("/customers/").get_data(as_text=True))

    def test_customers_edit_rejects_xss(self):
        db.session.add(Customer("Jan Kowalski", "Kraków", 30))
        db.session.commit()
        cid = Customer.query.one().id
        resp = self.client.post(f"/customers/{cid}/edit", data={
            "name": "Jan Kowalski", "city": XSS_PAYLOADS[2], "age": 30})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(Customer.query.one().city, "Kraków")

    def test_customers_create_accepts_valid(self):
        resp = self.client.post("/customers/create", data={
            "name": "Jan Kowalski", "city": "Kraków", "age": 30})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Customer.query.count(), 1)

    def test_loans_create_rejects_xss(self):
        db.session.add(Book("Pan Tadeusz", "Adam Mickiewicz", 1834, "5days"))
        db.session.commit()
        resp = self.client.post("/loans/create", data={
            "customer_name": XSS_PAYLOADS[0], "book_name": "Pan Tadeusz",
            "loan_date": "2024-01-01", "return_date": "2024-01-10"})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(Loan.query.count(), 0)
        self.assertEqual(Book.query.count(), 1)  # książka nie została "wypożyczona"
        self.assertNotIn("<script>", self.client.get("/loans/").get_data(as_text=True))

    def test_loans_create_accepts_valid(self):
        db.session.add(Book("Pan Tadeusz", "Adam Mickiewicz", 1834, "5days"))
        db.session.commit()
        resp = self.client.post("/loans/create", data={
            "customer_name": "Jan Kowalski", "book_name": "Pan Tadeusz",
            "loan_date": "2024-01-01", "return_date": "2024-01-10"})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Loan.query.count(), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
