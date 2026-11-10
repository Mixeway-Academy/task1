import pytest

from project.books.models import Book, validate_book_text
from project.customers.models import Customer, validate_customer_text
from project.loans.models import Loan, validate_loan_text


# books

def test_validate_book_text_accepts_valid():
    validate_book_text('Hobbajt', 'name')
    validate_book_text('Tolkien', 'author')


def test_validate_book_text_rejects_name_xss():
    with pytest.raises(ValueError):
        validate_book_text('<script>alert(1)</script>', 'name')

def test_validate_book_text_rejects_author_xss():
    with pytest.raises(ValueError):
        validate_book_text('<script>alert(1)</script>', 'author')

def test_book_create_accepts_valid():
    book = Book('Kapitan Bomba', 'Walaszek', 420, '2days')
    assert book.name == 'Kapitan Bomba'
    assert book.author == 'Walaszek'


def test_book_create_rejects_xss():
    with pytest.raises(ValueError):
        Book('<script>alert(1)</script>', 'Walaszek', 1927, '2days')


# customers 

def test_validate_customer_text_accepts_valid():
    validate_customer_text('Adam Malysz', 'name')
    validate_customer_text('Zakopane', 'city')


def test_validate_customer_text_rejects_name_xss():
    with pytest.raises(ValueError):
        validate_customer_text('<img src=x onerror=alert(1)>', 'name')

def test_validate_customer_text_rejects_city_xss():
    with pytest.raises(ValueError):
        validate_customer_text('<img src=x onerror=alert(1)>', 'city')

def test_customer_create_accepts_valid():
    customer = Customer('Jan Kowalski', 'Warszawa', 25)
    assert customer.name == 'Jan Kowalski'
    assert customer.city == 'Warszawa'


def test_customer_create_rejects_xss():
    with pytest.raises(ValueError):
        Customer('<script>alert(1)</script>', 'Warszawa', 25)


# loans

def test_validate_loan_text_accepts_valid():
    validate_loan_text('Jan Kowalski', 'customer_name')
    validate_loan_text('Hobbit', 'book_name')


def test_validate_loan_text_rejects_xss():
    with pytest.raises(ValueError):
        validate_loan_text('<script>alert(1)</script>', 'book_name')


def test_loan_create_accepts_valid():
    from datetime import datetime

    loan = Loan(
        customer_name='Jan Kowalski',
        book_name='Hobbit',
        loan_date=datetime(2024, 1, 1),
        return_date=datetime(2024, 1, 10),
        original_author='Tolkien',
        original_year_published=1937,
        original_book_type='2days',
    )
    assert loan.customer_name == 'Jan Kowalski'
    assert loan.book_name == 'Hobbit'


def test_loan_create_rejects_xss():
    from datetime import datetime

    with pytest.raises(ValueError):
        Loan(
            customer_name='Jan Kowalski',
            book_name='<script>alert(1)</script>',
            loan_date=datetime(2024, 1, 1),
            return_date=datetime(2024, 1, 10),
            original_author='Tolkien',
            original_year_published=1937,
            original_book_type='2days',
        )
