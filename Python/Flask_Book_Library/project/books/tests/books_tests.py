import unittest
from project.books.models import Book


class BooksTestsMethods(unittest.TestCase):
    def test_book_valid(self):
        book = Book("The Catcher in the Rye", "Jerome David Salinger", 1951, "Type")
        self.assertEqual(book.name, "The Catcher in the Rye")
        self.assertEqual(book.author, "Jerome David Salinger")

    def test_book_name_invalid(self):
        with self.assertRaises(ValueError):
            Book("<script>alert('XSS')</script>", "Jerome David Salinger", 1951, "Type")

    def test_book_author_invalid(self):
        with self.assertRaises(ValueError):
            Book("The Catcher in the Rye", "<script>alert('XSS')</script>", 1951, "Type")
