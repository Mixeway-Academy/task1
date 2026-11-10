import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from project import app, db
from project.books.models import Book


class BookModelTestCase(unittest.TestCase):
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

    def test_create_book_with_xss_payload_fails(self):
        with self.assertRaises(ValueError) as context:
            Book(
                name="<script>alert('XSS')</script>",
                author="John Doe",
                year_published=2023,
                book_type="5days"
            )

        self.assertIn("Book name contains invalid characters", str(context.exception))

    def test_edit_book_with_xss_payload_fails(self):
        valid_book = Book(
            name="Czysty Kod",
            author="Robert C Martin",
            year_published=2008,
            book_type="10days"
        )
        db.session.add(valid_book)
        db.session.commit()
        book_to_edit = Book.query.first()
        with self.assertRaises(ValueError) as context:
            book_to_edit.name = "<img src=x onerror=alert(1)>"

        self.assertIn("Book name contains invalid characters", str(context.exception))
        self.assertNotEqual(book_to_edit.name, "<img src=x onerror=alert(1)>")

    def test_create_book_success(self):
        new_book = Book(
            name="Wzorce Projektowe",
            author="Gang of Four",
            year_published=1994,
            book_type="10days"
        )
        db.session.add(new_book)
        db.session.commit()

        saved_book = Book.query.filter_by(name="Wzorce Projektowe").first()

        self.assertIsNotNone(saved_book)
        self.assertEqual(saved_book.author, "Gang of Four")
        self.assertEqual(saved_book.year_published, 1994)
        self.assertEqual(saved_book.book_type, "10days")
        self.assertEqual(saved_book.status, "available")

    def test_edit_book_success(self):
        book = Book(
            name="Domain Driven Design",
            author="Eric Evans",
            year_published=2003,
            book_type="5days"
        )
        db.session.add(book)
        db.session.commit()

        book_to_edit = Book.query.get(book.id)
        book_to_edit.name = "DDD Edycja Specjalna"
        book_to_edit.author = "Eric Evans"
        book_to_edit.year_published = 2020
        book_to_edit.book_type = "2days"

        db.session.commit()
        updated_book = Book.query.get(book.id)

        self.assertEqual(updated_book.name, "DDD Edycja Specjalna")
        self.assertEqual(updated_book.year_published, 2020)
        self.assertEqual(updated_book.book_type, "2days")

if __name__ == '__main__':
    unittest.main()