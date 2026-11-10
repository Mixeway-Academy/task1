import pytest
from project.models import Book


def create_valid_book():
    return Book(
        "Harry Potter",
        "J.K. Rowling",
        1997,
        "Fantasy"
    )


# Test poprawnego utworzenia książki
def test_valid_book():
    book = create_valid_book()

    assert book.name == "Harry Potter"
    assert book.author == "J.K. Rowling"
    assert book.year_published == 1997
    assert book.book_type == "Fantasy"
    assert book.status == "available"


# Test XSS w nazwie książki
def test_xss_in_name():
    with pytest.raises(ValueError):
        Book(
            "<script>alert('XSS')</script>",
            "J.K. Rowling",
            1997,
            "Fantasy"
        )


# Test XSS w autorze
def test_xss_in_author():
    with pytest.raises(ValueError):
        Book(
            "Harry Potter",
            "<script>alert('XSS')</script>",
            1997,
            "Fantasy"
        )


# Test XSS w typie książki
def test_xss_in_book_type():
    with pytest.raises(ValueError):
        Book(
            "Harry Potter",
            "J.K. Rowling",
            1997,
            "<script>alert('XSS')</script>"
        )


# Test XSS w statusie
def test_xss_in_status():
    with pytest.raises(ValueError):
        Book(
            "Harry Potter",
            "J.K. Rowling",
            1997,
            "Fantasy",
            "<script>alert('XSS')</script>"
        )


# Test pustej nazwy książki
def test_empty_name():
    with pytest.raises(ValueError):
        Book("", "J.K. Rowling", 1997, "Fantasy")


# Test pustego autora
def test_empty_author():
    with pytest.raises(ValueError):
        Book("Harry Potter", "", 1997, "Fantasy")


# Test pustego typu książki
def test_empty_book_type():
    with pytest.raises(ValueError):
        Book("Harry Potter", "J.K. Rowling", 1997, "")


# Test niepoprawnego roku wydania
def test_invalid_year():
    with pytest.raises(ValueError):
        Book("Harry Potter", "J.K. Rowling", "abc", "Fantasy")


# Test roku mniejszego od dozwolonego
def test_year_too_low():
    with pytest.raises(ValueError):
        Book("Harry Potter", "J.K. Rowling", 0, "Fantasy")


# Test roku większego od dozwolonego
def test_year_too_high():
    with pytest.raises(ValueError):
        Book("Harry Potter", "J.K. Rowling", 3000, "Fantasy")


# Test zbyt długiej nazwy książki
def test_name_too_long():
    with pytest.raises(ValueError):
        Book("A" * 65, "J.K. Rowling", 1997, "Fantasy")


# Test zbyt długiego autora
def test_author_too_long():
    with pytest.raises(ValueError):
        Book("Harry Potter", "A" * 65, 1997, "Fantasy")


# Test zbyt długiego typu książki
def test_book_type_too_long():
    with pytest.raises(ValueError):
        Book("Harry Potter", "J.K. Rowling", 1997, "A" * 21)


# Test niepoprawnego typu danych
def test_name_not_string():
    with pytest.raises(ValueError):
        Book(123, "J.K. Rowling", 1997, "Fantasy")


# Test przycinania białych znaków
def test_strip_whitespace():
    book = Book(
        "  Harry Potter  ",
        "  J.K. Rowling  ",
        1997,
        "  Fantasy  "
    )

    assert book.name == "Harry Potter"
    assert book.author == "J.K. Rowling"
    assert book.book_type == "Fantasy"
