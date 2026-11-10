import pytest
from project.books.models import Book

def test_valid_book():
    book = Book(
        "Harry Potter",
        "J.K. Rowling",
        1997,
        "5days"
    )

    assert book.name == "Harry Potter"


def test_reject_html_in_name():
    with pytest.raises(ValueError):
        Book(
            "<script>alert(1)</script>",
            "Test Author",
            2020,
            "5days"
        )


def test_reject_html_in_author():
    with pytest.raises(ValueError):
        Book(
            "Test Book",
            "<img src=x>",
            2020,
            "5days"
        )
