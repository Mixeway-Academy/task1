import unittest
from project.customers.models import Customer


class BooksTestsMethods(unittest.TestCase):
    def test_book_name_valid(self):
        customer = Customer("Some Customer", "City", 18)
        self.assertEquals(customer.name, "Some Customer")
        self.assertEquals(customer.city, "City")

    def test_book_name_invalid(self):
        with self.assertRaises(ValueError):
            Customer("<script>alert('XSS')</script>", "City", 18)

    def test_book_author_invalid(self):
        with self.assertRaises(ValueError):
            Customer("Some Customer", "<script>alert('XSS')</script>", 18)
