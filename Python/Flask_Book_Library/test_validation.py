import unittest
from project.books.models import Book
from project.customers.models import Customer

class TestSecurityValidation(unittest.TestCase):

    def test_valid_book_input_passes(self):
        """Scenariusz poprawny: Zwykłe dane nie powinny wyrzucać błędu."""
        try:
            book = Book(name="Wladca Pierscieni", author="J.R.R. Tolkien", year_published=1954, book_type="Fantasy")
            self.assertEqual(book.name, "Wladca Pierscieni")
        except ValueError:
            self.fail("Poprawne dane książki wyrzuciły wyjątek ValueError!")

    def test_invalid_book_input_fails(self):
        """Scenariusz niepoprawny (XSS): Złośliwe tagi w tytule książki powinny zostać zablokowane."""
        with self.assertRaises(ValueError):
            Book(name="<script>alert(1)</script>", author="Hacker", year_published=2023, book_type="IT")

    def test_valid_customer_input_passes(self):
        """Scenariusz poprawny dla klienta."""
        try:
            customer = Customer(name="Jan Kowalski", city="Warszawa", age=30)
            self.assertEqual(customer.name, "Jan Kowalski")
        except ValueError:
            self.fail("Poprawne dane klienta wyrzuciły wyjątek ValueError!")

    def test_invalid_customer_input_fails(self):
        """Scenariusz niepoprawny (XSS): Złośliwe tagi w nazwie klienta powinny zostać zablokowane."""
        with self.assertRaises(ValueError):
            Customer(name="<img src=x onerror=alert(1)>", city="Krakow", age=25)

if __name__ == '__main__':
    unittest.main()