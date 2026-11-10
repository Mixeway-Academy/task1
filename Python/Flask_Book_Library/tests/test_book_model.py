import pytest
from project.books.models import Book


def create_book(
    name="Władca Pierścieni",
    author="J.R.R. Tolkien",
    year_published=1954,
    book_type="Fantasy",
):
    return Book(
        name=name, author=author, year_published=year_published, book_type=book_type
    )


# Valid test cases for Book model
def test_create_book_valid():
    book = create_book()
    assert book.name == "Władca Pierścieni"
    assert book.author == "J.R.R. Tolkien"
    assert book.year_published == 1954
    assert book.book_type == "Fantasy"
    assert book.status == "available"


# XSS test cases for each book field
@pytest.mark.parametrize(
    "field, value",
    [
        ("name", "<script>alert('XSS')</script>"),
        ("author", "<script>alert('XSS')</script>"),
        ("book_type", "<script>alert('XSS')</script>"),
    ],
)
def test_create_book_xss(field, value):
    with pytest.raises(ValueError) as excinfo:
        kwargs = {}
        kwargs[field] = value
        create_book(**kwargs)
    assert "Input contains invalid characters." in str(excinfo.value)
