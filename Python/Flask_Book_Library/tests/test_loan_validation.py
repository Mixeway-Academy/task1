import unittest
from datetime import datetime
from project.loans.models import Loan

class TestLoanValidation(unittest.TestCase):
    def create_loan(self, customer_name, book_name):
        return Loan(
            customer_name=customer_name,
            book_name=book_name,
            loan_date=datetime(2026, 11, 10),
            return_date=datetime(2026, 11, 20),
            original_author="Rick Riordan",
            original_year_published=1997,
            original_book_type="5days"
        )

    def test_valid_loan(self):
        loan = self.create_loan("Jan Kowalski", "Percy Jackson")
        self.assertEqual(loan.customer_name, "Jan Kowalski")
        self.assertEqual(loan.book_name, "Percy Jackson")

    def test_text_with_spaces(self):
        loan = self.create_loan("  Jan Kowalski  ", "  Percy Jackson  ")

        self.assertEqual(loan.customer_name, "Jan Kowalski")
        self.assertEqual(loan.book_name, "Percy Jackson")

    def test_xss_in_customer_name(self):
        with self.assertRaises(ValueError):
            self.create_loan("<script>alert('anothervulnerability')</script>", "Percy Jackson")

    def test_xss_in_book_name(self):
        with self.assertRaises(ValueError):
            self.create_loan("Jan Kowalski", "<script>alert('anothervulnerability')</script>")
