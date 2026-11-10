import unittest
from datetime import datetime

from project.books.models import Book
from project.customers.models import Customer
from project.input_validation import validate_plain_text
from project.loans.models import Loan


class PlainTextValidationTests(unittest.TestCase):
    def test_accepts_ordinary_text_without_changing_it(self):
        for value in ("O'Reilly & Sons - Łódź, 1 < 2 > 0", 'Niedomknięty <svg'):
            with self.subTest(value=value):
                self.assertEqual(validate_plain_text('name', value), value)

    def test_rejects_html_tags(self):
        payloads = (
            '<script>alert(1)</script>',
            '<img src=x onerror=alert(1)>',
            '<svg/onload=alert(1)>',
            '<iframe src=javascript:alert(1)>',
            'Zamknięcie </td>',
        )
        for payload in payloads:
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                validate_plain_text('name', payload)

    def test_book_rejects_unsafe_text_on_create_and_edit(self):
        with self.assertRaises(ValueError):
            Book('Książka', '<img src=x onerror=alert(1)>', 2024, '2days')

        book = Book('Książka', 'Jan Kowalski', 2024, '2days')
        for field in ('name', 'author'):
            with self.subTest(field=field), self.assertRaises(ValueError):
                setattr(book, field, '<svg/onload=alert(1)>')

    def test_customer_rejects_unsafe_text_on_create_and_edit(self):
        with self.assertRaises(ValueError):
            Customer('Klient', '<script>alert(1)</script>', 25)

        customer = Customer('Klient', 'Łódź', 25)
        for field in ('name', 'city'):
            with self.subTest(field=field), self.assertRaises(ValueError):
                setattr(customer, field, '<svg/onload=alert(1)>')

    def test_loan_rejects_unsafe_text_on_create_and_edit(self):
        now = datetime(2026, 11, 10)
        with self.assertRaises(ValueError):
            Loan('<svg/onload=alert(1)>', 'Książka', now, now,
                 'Jan Kowalski', 2024, '2days')

        loan = Loan('Klient', 'Książka', now, now, 'Jan Kowalski', 2024, '2days')
        for field in ('customer_name', 'book_name'):
            with self.subTest(field=field), self.assertRaises(ValueError):
                setattr(loan, field, '<svg/onload=alert(1)>')


if __name__ == '__main__':
    unittest.main()
