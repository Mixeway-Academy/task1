import unittest
from datetime import datetime
from project.books.models import Book
from project.customers.models import Customer
from project.loans.models import Loan

class TestXSS(unittest.TestCase):

    xss_payloads = [
        "<script>alert('1')</script>",
        "%3Cscript%3Ealert('XSS')%3C/script%3E",
        "<img src=x onerror='alert(\"XSS\")'>",
        "<svg/onload=alert('XSS')>",
        "<input onfocus=javascript:alert(1) autofocus>"
        "<<SCRIPT>alert('XSS');//<</SCRIPT>",
        "\u003Cscript\u003Ealert('XSS')\u003C/script\u003E",
    ]

    def test_book_name_xss(self):
        for payload in self.xss_payloads:
            with self.assertRaises(ValueError):
                Book(name=payload, author="PoprawnyAutor", year_published=2012, book_type="5days")

    def test_book_author_xss(self):
        for payload in self.xss_payloads:
            with self.assertRaises(ValueError):
                Book(name="PoprawneImie", author=payload, year_published=2012, book_type="5days")

    def test_customer_name_xss(self):
        for payload in self.xss_payloads:
            with self.assertRaises(ValueError):
                Customer(name=payload, city="PoprawneMiasto", age=123)

    def test_customer_city_xss(self):
        for payload in self.xss_payloads:
            with self.assertRaises(ValueError):
                Customer(name="PoprawnyKlient", city=payload, age=123)

    def test_loan_customer_name_xss(self):
        loan_date = datetime.now()
        return_date = datetime.now()
        for payload in self.xss_payloads:
            with self.assertRaises(ValueError):
                Loan(customer_name=payload, book_name="PoprawnaNazwaKsiazki", loan_date=loan_date, return_date=return_date, original_author="PoprawnyAutor",
				original_year_published=2044, original_book_type="5days")

    def test_loan_book_name_xss(self):
        loan_date = datetime.now()
        return_date = datetime.now()
        for payload in self.xss_payloads:
            with self.assertRaises(ValueError):
                Loan(customer_name="PoprawnaNazwaKlienta", book_name=payload, loan_date=loan_date, return_date=return_date, original_author="PoprawnyAutor", original_year_published=2044, original_book_type="5days")

    def test_valid_book(self):
        try:
            Book(name="PoprawnaNazwaKsiazki", author="PoprawnyAutor", year_published=1999, book_type="5days")
        except ValueError:
            self.fail("ValueError dla klasy Book!")

    def test_valid_customer(self):
        try:
            Customer(name="PoprawnaNazwaKlienta", city="ValidCity", age=30)
        except ValueError:
            self.fail("ValueError dla klasy Customer")

    def test_valid_loan(self):
        loan_date = datetime.now()
        return_date = datetime.now()
        try:
            Loan(customer_name="PoprawnaNazwaKlienta", book_name="PoprawnaNazwaKsiazki", loan_date=loan_date, return_date=return_date, original_author="PoprawnyAutor", original_year_published=2000, original_book_type="5days")
        except ValueError:
            self.fail("ValueError dla klasy Loan")


if __name__ == "__main__":
    unittest.main()
