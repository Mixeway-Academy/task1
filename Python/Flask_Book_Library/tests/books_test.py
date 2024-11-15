"""Books Validator Tests"""

import unittest

from project.books.models import Book, BookChecker

correct_input = {
    "name": "Book Name",
    "author": "Author Name",
    "year_published": 2021,
    "book_type": "2days",
    "status": "available",
}
xss_input = {
    "name": "<script>alert('xss')</script>",
    "author": "<script>alert('xss')</script>",
    "year_published": "<script>alert('xss')</script>",
    "book_type": "<script>alert('xss')</script>",
    "status": "<script>alert('xss')</script>",
}
invalid_input = {
    "year_published": "abc",
    "book_type": "123",
}


class TestBookModel(unittest.TestCase):

    def test_book_model(self):
        book = Book(**correct_input)
        self.assertEqual(book.name, correct_input["name"])
        self.assertEqual(book.author, correct_input["author"])
        self.assertEqual(book.year_published, correct_input["year_published"])
        self.assertEqual(book.book_type, correct_input["book_type"])
        self.assertEqual(book.status, correct_input["status"])

    def test_book_model_xss(self):
        with self.assertRaises(ValueError):
            book = Book(**xss_input)

        # test for invalid name

    def test_name(self):
        input = correct_input.copy()
        input["year_published"] = invalid_input["year_published"]
        with self.assertRaises(ValueError):
            book = Book(**input)

    def test_booktype(self):
        input = correct_input.copy()
        input["book_type"] = invalid_input["book_type"]
        with self.assertRaises(ValueError):
            book = Book(**input)
