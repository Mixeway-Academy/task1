import unittest
from datetime import date
from project.loans.models import Loan


class BooksTestsMethods(unittest.TestCase):
    def test_loan_valid(self):
        loan = Loan("Some Customer", "The Catcher in the Rye", date(2023, 11, 12),
                    date(2023, 11, 13), "Jerome David Salinger", 1951, "Type")
        self.assertEqual(loan.customer_name, "Some Customer")
        self.assertEqual(loan.book_name, "The Catcher in the Rye")
        self.assertEqual(loan.original_author, "Jerome David Salinger")

    def test_customer_name_invalid(self):
        with self.assertRaises(ValueError):
            Loan("<script>alert('XSS')</script>", "The Catcher in the Rye", date(2023, 11, 12),
                 date(2023, 11, 13), "Jerome David Salinger", 1951, "Type")

    def test_book_name_invalid(self):
        with self.assertRaises(ValueError):
            Loan("Some Customer", "<script>alert('XSS')</script>", date(2023, 11, 12),
                 date(2023, 11, 13), "Jerome David Salinger", 1951, "Type")

    def test_original_author_invalid(self):
        with self.assertRaises(ValueError):
            Loan("Some Customer", "The Catcher in the Rye", date(2023, 11, 12),
                 date(2023, 11, 13), "<script>alert('XSS')</script>", 1951, "Type")
