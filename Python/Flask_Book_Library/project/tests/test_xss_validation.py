import unittest
import html
from project.books.models import Book
from project import app, db

class XSSValidationTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_book_creation_sanitizes_input(self):
        malicious_name = "<script>alert('XSS in name')</script>"
        malicious_author = "<img src=x onerror=alert('XSS in author')>"
        expected_name = html.escape(malicious_name)
        expected_author = html.escape(malicious_author)

        # Act
        with app.app_context():
            book = Book(
                name=malicious_name,
                author=malicious_author,
                year_published=2023,
                book_type='5days'
            )
            db.session.add(book)
            db.session.commit()

            retrieved_book = Book.query.first()
            self.assertIsNotNone(retrieved_book)
            self.assertEqual(retrieved_book.name, expected_name)
            self.assertEqual(retrieved_book.author, expected_author)
            print(f"\nOriginal Name: {malicious_name}")
            print(f"Sanitized Name: {retrieved_book.name}")
            print(f"Original Author: {malicious_author}")
            print(f"Sanitized Author: {retrieved_book.author}")

if __name__ == '__main__':
    unittest.main()
