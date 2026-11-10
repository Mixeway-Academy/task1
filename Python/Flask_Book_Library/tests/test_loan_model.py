import pytest
from project.loans.models import Loan


def create_loan(
    customer_name="Jan Kowalski",
    book_name="Władca Pierścieni",
    loan_date="2023-01-01 10:00:00",
    return_date="2023-01-15 10:00:00",
    original_author="J.R.R. Tolkien",
    original_year_published=1954,
    original_book_type="Fantasy",
):
    return Loan(
        customer_name=customer_name,
        book_name=book_name,
        loan_date=loan_date,
        return_date=return_date,
        original_author=original_author,
        original_year_published=original_year_published,
        original_book_type=original_book_type,
    )


# Valid test cases for Loan model
def test_create_loan_valid():
    loan = create_loan()
    assert loan.customer_name == "Jan Kowalski"
    assert loan.book_name == "Władca Pierścieni"
    assert loan.loan_date == "2023-01-01 10:00:00"
    assert loan.return_date == "2023-01-15 10:00:00"
    assert loan.original_author == "J.R.R. Tolkien"
    assert loan.original_year_published == 1954
    assert loan.original_book_type == "Fantasy"


# XSS test cases for each loan field
@pytest.mark.parametrize(
    "field, value",
    [
        ("customer_name", "<script>alert('XSS')</script>"),
        ("book_name", "<script>alert('XSS')</script>"),
        ("original_author", "<script>alert('XSS')</script>"),
        ("original_book_type", "<script>alert('XSS')</script>"),
    ],
)
def test_create_loan_xss(field, value):
    with pytest.raises(ValueError) as excinfo:
        kwargs = {}
        kwargs[field] = value
        create_loan(**kwargs)
    assert "Input contains invalid characters." in str(excinfo.value)
