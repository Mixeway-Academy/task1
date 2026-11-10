import unittest
from datetime import datetime

from flask import Flask
from project import app as original_app, db
from project.books.models import Book
from project.customers.models import Customer
from project.loans.models import Loan


PAYLOADS = (
    "<script>alert(1)</script>",
    "<img src=x onerror=alert(1)>",
    "<svg onload=alert(1)>",
    "<ScRiPt>alert(1)</ScRiPt>",
)


class ValidationTests(unittest.TestCase):
    def test_models_accept_plain_text(self):
        book = Book("Pan Tadeusz", "Adam Mickiewicz", 1834, "5days")
        self.assertEqual(book.name, "Pan Tadeusz")
        self.assertEqual(book.author, "Adam Mickiewicz")
        for author in ("", "   ", None):
            self.assertEqual(Book("Pan Tadeusz", author, 1834, "5days").author, author)
        self.assertEqual(Customer("Piotr Jabłoński", "Łódź", 30).city, "Łódź")

    def test_text_length_boundary_and_punctuation(self):
        name = "Pan Tadeusz".ljust(64, ".")
        book = Book(name, "Adam Mickiewicz", 1834, "5days")
        self.assertEqual(book.name, name)
        book.author = "Adam Mickiewicz".ljust(64, ".")
        self.assertEqual(len(book.author), 64)
        customer = Customer("Piotr Jabłoński", "Łódź", 30)
        customer.city = "Bielsko-Biała / Łódź & okolice"
        self.assertEqual(customer.city, "Bielsko-Biała / Łódź & okolice")

    def test_creation_and_assignment_reject_invalid_text(self):
        now = datetime(2024, 1, 1)
        cases = (
            (
                Book,
                dict(
                    name="Pan Tadeusz",
                    author="Adam Mickiewicz",
                    year_published=1834,
                    book_type="5days",
                ),
                ("name", "author"),
            ),
            (
                Customer,
                dict(
                    name="Piotr Jabłoński",
                    city="Łódź",
                    age=30,
                ),
                ("name", "city"),
            ),
            (
                Loan,
                dict(
                    customer_name="Piotr Jabłoński",
                    book_name="Pan Tadeusz",
                    loan_date=now,
                    return_date=now,
                    original_author="Adam Mickiewicz",
                    original_year_published=1834,
                    original_book_type="5days",
                ),
                ("customer_name", "book_name"),
            ),
        )
        for cls, data, fields in cases:
            for field in fields:
                for value in (*PAYLOADS, 123, [], {}, None, "", "   ", "a" * 65):
                    if field == "author" and value in (None, "", "   "):
                        continue
                    with self.subTest(model=cls.__name__, field=field, value=value):
                        with self.assertRaises(ValueError):
                            cls(**dict(data, **{field: value}))
                        obj = cls(**data)
                        with self.assertRaises(ValueError):
                            setattr(obj, field, value)
                        self.assertEqual(getattr(obj, field), data[field])


class RouteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__, template_folder=original_app.root_path + "/templates")
        cls.app.config.update(
            TESTING=True,
            SECRET_KEY="test",
            SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        )
        db.init_app(cls.app)
        for blueprint in original_app.blueprints.values():
            cls.app.register_blueprint(blueprint)

    def setUp(self):
        self.context = self.app.app_context()
        self.context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.context.pop()

    def test_books_and_customers_create_and_edit(self):
        cases = (
            (
                "books",
                Book,
                dict(
                    name="Pan Tadeusz",
                    author="Adam Mickiewicz",
                    year_published=1834,
                    book_type="5days",
                ),
                ("name", "author"),
                "json",
            ),
            (
                "customers",
                Customer,
                dict(
                    name="Piotr Jabłoński",
                    city="Łódź",
                    age="30",
                ),
                ("name", "city"),
                "data",
            ),
        )
        for path, model, data, fields, encoding in cases:
            for field in fields:
                for payload in PAYLOADS:
                    response = self.client.post(
                        f"/{path}/create", **{encoding: dict(data, **{field: payload})}
                    )
                    self.assertEqual(response.status_code, 400)
                    self.assertIn("error", response.json)
                    self.assertEqual(model.query.count(), 0)
            self.assertEqual(
                self.client.post(f"/{path}/create", **{encoding: data}).status_code, 302
            )
            obj = model.query.one()
            for field in fields:
                response = self.client.post(
                    f"/{path}/{obj.id}/edit",
                    **{encoding: {**data, "name": "Changed", field: PAYLOADS[0]}},
                )
                self.assertEqual(response.status_code, 400)
                db.session.expire_all()
                self.assertEqual(model.query.one().name, data["name"])
                self.assertEqual(getattr(model.query.one(), field), data[field])
            self.assertEqual(
                self.client.post(
                    f"/{path}/{obj.id}/edit", **{encoding: dict(data, name="Changed")}
                ).status_code,
                200 if path == "books" else 302,
            )
            self.assertEqual(model.query.one().name, "Changed")
        self.assertEqual(
            self.client.post(
                "/books/1/edit", json={"author": "Adam Mickiewicz"}
            ).status_code,
            200,
        )
        self.assertEqual(Book.query.one().name, "Changed")

    def test_loan_rejection_preserves_book(self):
        db.session.add(Book("Pan Tadeusz", "Adam Mickiewicz", 1834, "5days"))
        db.session.commit()
        response = self.client.post(
            "/loans/create",
            data=dict(
                customer_name=PAYLOADS[0],
                book_name="Pan Tadeusz",
                loan_date="2024-01-01",
                return_date="2024-01-02",
            ),
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Loan.query.count(), 0)
        self.assertEqual(Book.query.count(), 1)
        response = self.client.post(
            "/loans/create",
            data=dict(
                customer_name="Piotr Jabłoński",
                book_name="Pan Tadeusz",
                loan_date="2024-01-01",
                return_date="2024-01-02",
            ),
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Loan.query.count(), 1)
        self.assertEqual(Book.query.count(), 0)


if __name__ == "__main__":
    unittest.main()
