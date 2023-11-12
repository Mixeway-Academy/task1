import unittest
from project.books.models import Book


class BooksTestsMethods(unittest.TestCase):
    def test_book_name_valid(self):
        book = Book("Buszujący w Zbożu", "Jerome David Salinger", 1951, "Type")
        self.assertEquals(book.name, "Buszujący w Zbożu")
        self.assertEquals(book.author, "Jerome David Salinger")

    def test_book_name_invalid(self):
        with self.assertRaises(ValueError):
            Book("<script>alert('XSS')</script>", "Jerome David Salinger", 1951, "Type")

    def test_book_author_invalid(self):
        with self.assertRaises(ValueError):
            Book("Buszujący w Zbożu", "<script>alert('XSS')</script>", 1951, "Type")
