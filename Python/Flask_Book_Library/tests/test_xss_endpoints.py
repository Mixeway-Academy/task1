"""Endpoint tests: XSS payloads get HTTP 400 and are not stored. Run: python -m unittest discover -s tests -v"""
import os
import unittest

os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")

from project import app, db  # noqa: E402
from project.books.models import Book  # noqa: E402
from project.customers.models import Customer  # noqa: E402
from project.loans.models import Loan  # noqa: E402

XSS = "<img src=x onerror=alert(1)>"


class EndpointTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.ctx = app.app_context()
        self.ctx.push()
        db.drop_all()
        db.create_all()
        self.client = app.test_client()

    def tearDown(self):
        db.session.remove()
        self.ctx.pop()

    def add_book(self, name="Solaris"):
        book = Book(name=name, author="Stanisław Lem", year_published=1961, book_type="5days")
        db.session.add(book)
        db.session.commit()
        return book

    def add_customer(self, name="Jan Kowalski"):
        customer = Customer(name=name, city="Warszawa", age=30)
        db.session.add(customer)
        db.session.commit()
        return customer


class BookEndpointsTest(EndpointTestCase):
    def test_create_valid_book(self):
        resp = self.client.post("/books/create", json={
            "name": "Pan Tadeusz", "author": "Adam Mickiewicz", "year_published": "1834", "book_type": "2days"})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Book.query.count(), 1)

    def test_create_book_with_xss_is_rejected(self):
        for field in ("name", "author"):
            with self.subTest(field=field):
                payload = {"name": "Pan Tadeusz", "author": "Adam Mickiewicz", "year_published": "1834", "book_type": "2days"}
                payload[field] = XSS
                resp = self.client.post("/books/create", json=payload)
                self.assertEqual(resp.status_code, 400)
                self.assertIn("Invalid input", resp.get_json()["error"])
        self.assertEqual(Book.query.count(), 0)
        self.assertNotIn(b"onerror", self.client.get("/books/").data)

    def test_create_book_with_invalid_year_or_type_is_rejected(self):
        base = {"name": "Pan Tadeusz", "author": "Adam Mickiewicz", "year_published": "1834", "book_type": "2days"}
        for field, value in (("year_published", "<script>"), ("year_published", "3000"), ("book_type", XSS)):
            with self.subTest(field=field, value=value):
                resp = self.client.post("/books/create", json={**base, field: value})
                self.assertEqual(resp.status_code, 400)
        self.assertEqual(Book.query.count(), 0)

    def test_create_book_with_missing_fields_is_rejected(self):
        resp = self.client.post("/books/create", json={"name": "Pan Tadeusz"})
        self.assertEqual(resp.status_code, 400)

    def test_edit_book_with_xss_is_rejected(self):
        book_id = self.add_book().id
        resp = self.client.post(f"/books/{book_id}/edit", json={"author": XSS})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(db.session.get(Book, book_id).author, "Stanisław Lem")

    def test_edit_book_valid(self):
        book_id = self.add_book().id
        resp = self.client.post(f"/books/{book_id}/edit", json={"name": "Solaris (wyd. 2)"})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(db.session.get(Book, book_id).name, "Solaris (wyd. 2)")


class CustomerEndpointsTest(EndpointTestCase):
    def test_create_valid_customer(self):
        resp = self.client.post("/customers/create", data={"name": "Anna Nowak", "city": "Kraków", "age": "25"})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Customer.query.count(), 1)

    def test_create_customer_with_xss_is_rejected(self):
        for field in ("name", "city"):
            with self.subTest(field=field):
                payload = {"name": "Anna Nowak", "city": "Kraków", "age": "25"}
                payload[field] = XSS
                resp = self.client.post("/customers/create", data=payload)
                self.assertEqual(resp.status_code, 400)
        self.assertEqual(Customer.query.count(), 0)
        self.assertNotIn(b"onerror", self.client.get("/customers/").data)

    def test_edit_customer_with_xss_is_rejected(self):
        customer_id = self.add_customer().id
        resp = self.client.post(f"/customers/{customer_id}/edit",
                                data={"name": XSS, "city": "Warszawa", "age": "30"})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(db.session.get(Customer, customer_id).name, "Jan Kowalski")


class LoanEndpointsTest(EndpointTestCase):
    def loan_form(self, customer_name, book_name="Solaris"):
        return {"customer_name": customer_name, "book_name": book_name,
                "loan_date": "2026-11-01", "return_date": "2026-11-10"}

    def test_create_valid_loan(self):
        self.add_book()
        self.add_customer()
        resp = self.client.post("/loans/create", data=self.loan_form("Jan Kowalski"))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Loan.query.count(), 1)

    def test_create_loan_with_xss_customer_name_is_rejected(self):
        self.add_book()
        resp = self.client.post("/loans/create", data=self.loan_form(XSS))
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(Loan.query.count(), 0)
        # a rejected loan must not remove the book
        self.assertEqual(Book.query.count(), 1)
        self.assertNotIn(b"onerror", self.client.get("/loans/").data)


if __name__ == "__main__":
    unittest.main()
