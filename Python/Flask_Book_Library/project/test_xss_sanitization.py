import unittest
from project.books.models import Book
from project.customers.models import Customer


class TestXSSSanitization(unittest.TestCase):

    def test_book_model_sanitization(self):
        # Input with potential XSS
        malicious_name = "<script>alert('XSS')</script>"
        malicious_author = "<img src=x onerror=alert('XSS')>"

        # Create a book instance
        book = Book(name=malicious_name, author=malicious_author, year_published=2022, book_type="Fiction")

        # Verify that XSS is sanitized
        self.assertNotIn("<script>", book.name)
        self.assertNotIn("<img>", book.author)
        self.assertIn("&lt;script&gt;", book.name)
        self.assertIn("&lt;img&#32;src&#61;x&#32;onerror&#61;alert(&apos;XSS&apos;)&gt;", book.author)

    def test_customer_model_sanitization(self):
        # Input with potential XSS
        malicious_name = "<script>alert('XSS')</script>"
        malicious_city = "<img src=x onerror=alert('XSS')>"

        # Create a customer instance
        customer = Customer(name=malicious_name, city=malicious_city, age=25)

        # Verify that XSS is sanitized
        self.assertNotIn("<script>", customer.name)
        self.assertNotIn("<img>", customer.city)
        self.assertIn("&lt;script&gt;", customer.name)
        self.assertIn("&lt;img src=x onerror=alert(&#39;XSS&#39;)&gt;", customer.city)


if __name__ == '__main__':
    unittest.main()
