import unittest
from datetime import date, datetime

from loader import load

validators = load('project.loans.validators')
ValidationError = validators.ValidationError

LV = validators.LOAN_VALIDATORS


class LoanTextFieldTests(unittest.TestCase):
    def test_valid_values_are_accepted(self):
        cases = {
            'customer_name': "Jan Kowalski",
            'book_name': "Harry Potter & the Philosopher's Stone",
            'original_author': "J.R.R. Tolkien",
            'original_year_published': 1999,
            'original_book_type': "5days",
        }
        for field, value in cases.items():
            with self.subTest(field=field):
                self.assertEqual(LV[field](value), value)

    def test_xss_payloads_are_rejected_in_every_text_field(self):
        payloads = ["<script>alert(1)</script>", "<img src=x onerror=alert(1)>", '" onmouseover="alert(1)']
        for field in ('customer_name', 'book_name', 'original_author', 'original_book_type'):
            for payload in payloads:
                with self.subTest(field=field, payload=payload):
                    with self.assertRaises(ValidationError):
                        LV[field](payload)

    def test_invalid_year_and_type_are_rejected(self):
        for field, value in [('original_year_published', "<script>"), ('original_year_published', 0),
                             ('original_year_published', None), ('original_book_type', "1day"),
                             ('customer_name', None), ('book_name', ""), ('original_author', "")]:
            with self.subTest(field=field, value=value):
                with self.assertRaises(ValidationError):
                    LV[field](value)

    def test_error_message_names_the_loan_field(self):
        with self.assertRaisesRegex(ValidationError, r"^customer_name: "):
            LV['customer_name']("<b>")
        with self.assertRaisesRegex(ValidationError, r"^book_name: "):
            LV['book_name']("<b>")
        with self.assertRaisesRegex(ValidationError, r"^original_author: "):
            LV['original_author']("<b>")


class LoanDateTests(unittest.TestCase):
    def test_valid_dates_are_accepted_unchanged(self):
        for value in [date(2026, 11, 10), datetime(2026, 11, 10, 12, 30), date(1900, 1, 1), date(2100, 12, 31)]:
            for validator in (validators.validate_loan_date, validators.validate_return_date):
                with self.subTest(value=value, validator=validator.__name__):
                    self.assertEqual(validator(value), value)

    def test_invalid_dates_are_rejected(self):
        for value in ["2026-11-10", "<script>alert(1)</script>", None, 20261110, 1.5, True,
                      date(1899, 12, 31), date(2101, 1, 1), datetime(1800, 1, 1)]:
            for validator in (validators.validate_loan_date, validators.validate_return_date):
                with self.subTest(value=value, validator=validator.__name__):
                    with self.assertRaises(ValidationError):
                        validator(value)


class LoanPeriodTests(unittest.TestCase):
    def test_return_on_or_after_loan_date_is_accepted(self):
        validators.validate_loan_period(date(2026, 11, 10), date(2026, 11, 20))
        validators.validate_loan_period(date(2026, 11, 10), date(2026, 11, 10))
        validators.validate_loan_period(datetime(2026, 11, 10, 18, 0), datetime(2026, 11, 10, 9, 0))
        validators.validate_loan_period(date(2026, 11, 10), datetime(2026, 11, 11, 8, 0))

    def test_return_before_loan_date_is_rejected(self):
        with self.assertRaises(ValidationError):
            validators.validate_loan_period(date(2026, 11, 10), date(2026, 11, 9))
        with self.assertRaises(ValidationError):
            validators.validate_loan_period(datetime(2026, 11, 10, 8, 0), date(2026, 11, 9))

    def test_non_dates_are_rejected(self):
        with self.assertRaises(ValidationError):
            validators.validate_loan_period(None, date(2026, 11, 10))
        with self.assertRaises(ValidationError):
            validators.validate_loan_period(date(2026, 11, 10), "2026-11-11")


class ModuleContractTests(unittest.TestCase):
    def test_every_loan_field_has_a_validator(self):
        self.assertEqual(set(LV), {'customer_name', 'book_name', 'loan_date', 'return_date',
                                   'original_author', 'original_year_published', 'original_book_type'})


if __name__ == '__main__':
    unittest.main()