import pytest
from datetime import datetime
from project.models import Loan


def create_valid_loan():
    return Loan(
        "Jan Kowalski",
        "Harry Potter",
        datetime(2025, 1, 10),
        datetime(2025, 1, 20),
        "J.K. Rowling",
        1997,
        "Fantasy"
    )


def test_valid_loan():
    loan = create_valid_loan()

    assert loan.customer_name == "Jan Kowalski"
    assert loan.book_name == "Harry Potter"
    assert loan.original_year_published == 1997


def test_xss_in_customer_name():
    with pytest.raises(ValueError):
        Loan(
            "<script>alert('XSS')</script>",
            "Harry Potter",
            datetime(2025, 1, 10),
            datetime(2025, 1, 20),
            "J.K. Rowling",
            1997,
            "Fantasy"
        )


def test_xss_in_book_name():
    with pytest.raises(ValueError):
        Loan(
            "Jan Kowalski",
            "<script>alert('XSS')</script>",
            datetime(2025, 1, 10),
            datetime(2025, 1, 20),
            "J.K. Rowling",
            1997,
            "Fantasy"
        )


def test_invalid_year():
    with pytest.raises(ValueError):
        Loan(
            "Jan Kowalski",
            "Harry Potter",
            datetime(2025, 1, 10),
            datetime(2025, 1, 20),
            "J.K. Rowling",
            "abc",
            "Fantasy"
        )


def test_return_date_before_loan_date():
    with pytest.raises(ValueError):
        Loan(
            "Jan Kowalski",
            "Harry Potter",
            datetime(2025, 1, 20),
            datetime(2025, 1, 10),
            "J.K. Rowling",
            1997,
            "Fantasy"
        )


def test_empty_customer_name():
    with pytest.raises(ValueError):
        Loan(
            "",
            "Harry Potter",
            datetime(2025, 1, 10),
            datetime(2025, 1, 20),
            "J.K. Rowling",
            1997,
            "Fantasy"
        )


def test_invalid_date():
    with pytest.raises(ValueError):
        Loan(
            "Jan Kowalski",
            "Harry Potter",
            "niepoprawna-data",
            datetime(2025, 1, 20),
            "J.K. Rowling",
            1997,
            "Fantasy"
        )
