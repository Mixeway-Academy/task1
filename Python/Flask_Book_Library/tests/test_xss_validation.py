from datetime import datetime
import unittest
from project import app, db
from project.books.models import Book
from project.customers.models import Customer
from project.loans.models import Loan


class TestXSSValidation(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_valid_book_creation(self):
        book = Book(
            name="Rok 1984: Wydanie II",
            author="Charlotte Brontë",
            year_published=1949,
            book_type="5days"
        )
        self.assertEqual(book.name, "Rok 1984: Wydanie II")
        self.assertEqual(book.author, "Charlotte Brontë")

    def test_book_xss_in_name_rejected(self):
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert(1)>",
            "<svg/onload=alert(1)>",
            "Book\"><script>alert(1)</script>"
        ]
        for payload in xss_payloads:
            with self.subTest(payload=payload):
                with self.assertRaises(ValueError):
                    Book(
                        name=payload,
                        author="Valid Author",
                        year_published=2023,
                        book_type="2days"
                    )

    def test_book_xss_in_author_rejected(self):
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert(1)>",
            "Author<b>",
            "Author123"
        ]
        for payload in xss_payloads:
            with self.subTest(payload=payload):
                with self.assertRaises(ValueError):
                    Book(
                        name="Valid Book",
                        author=payload,
                        year_published=2023,
                        book_type="2days"
                    )

    def test_valid_customer_creation(self):
        customer = Customer(name="Jan Kowalski", city="Bielsko-Biała", age=30)
        self.assertEqual(customer.name, "Jan Kowalski")
        self.assertEqual(customer.city, "Bielsko-Biała")

    def test_customer_xss_rejected(self):
        with self.assertRaises(ValueError):
            Customer(name="<script>alert(1)</script>", city="Warszawa", age=25)

        with self.assertRaises(ValueError):
            Customer(name="Jan Kowalski", city="<img src=x onerror=alert(1)>", age=25)

    def test_loan_xss_rejected(self):
        now = datetime.now()
        with self.assertRaises(ValueError):
            Loan(
                customer_name="<script>alert(1)</script>",
                book_name="Clean Code",
                loan_date=now,
                return_date=now,
                original_author="Robert C. Martin",
                original_year_published=2008,
                original_book_type="5days"
            )

        with self.assertRaises(ValueError):
            Loan(
                customer_name="Jan Kowalski",
                book_name="<img src=x onerror=alert(1)>",
                loan_date=now,
                return_date=now,
                original_author="Robert C. Martin",
                original_year_published=2008,
                original_book_type="5days"
            )


if __name__ == "__main__":
    unittest.main()
