import pytest
from project.books.models import Book

@pytest.mark.parametrize("valid_name", [
    "Długi tytuł książki z podtytułem: Część 1",
    "Rok 1984",
    "Gwiezdne Wojny: Część V (Imperium kontratakuje)",
    "Władca Pierścieni. Drużyna Pierścienia.",
    "Odprawa posłów greckich",
    "Jądro Ciemności—Historia Prawdziwa",
])
def test_book_name_valid(valid_name):
    try:
        Book(name=valid_name, author="W. Shakespeare", year_published=2000, book_type="Fiction")
    except ValueError:
        pytest.fail(f"Walidacja nie powinna odrzucić prawidłowego tytułu: {valid_name}")

@pytest.mark.parametrize("invalid_name", [
    "",
    "Tytuł z $ symbolem",
    "Tytuł z % symbolem",
])
def test_book_name_invalid(invalid_name):
    with pytest.raises(ValueError, match="Invalid book name."):
        Book(name=invalid_name, author="W. Shakespeare", year_published=2000, book_type="Fiction")


@pytest.mark.parametrize("malicious_name", [
    "<script>alert('XSS')</script>",
    "\" onmouseover='alert(1)'",
    "Book Name <img src=x onerror=alert(1)>",
    "Tytuł z tagiem <h1>",
    "' OR 1=1 --",
    "SELECT * FROM books",
])
def test_book_name_security_rejected(malicious_name):
    with pytest.raises(ValueError, match="Invalid book name."):
        Book(name=malicious_name, author="Valid Author", year_published=2000, book_type="Fiction")


@pytest.mark.parametrize("valid_author", [
    "Jan Kowalski",
    "Maria Skłodowska-Curie",
    "J. R. R. Tolkien",
    "O'Malley",
    "F. Scott Fitzgerald",
    "Łukasz P.",
])
def test_author_name_valid(valid_author):
    try:
        Book(name="Valid Title", author=valid_author, year_published=2000, book_type="Fiction")
    except ValueError:
        pytest.fail(f"Walidacja nie powinna odrzucić prawidłowego autora: {valid_author}")

@pytest.mark.parametrize("invalid_author", [
    "Autor z cyfrą 1",
    "Autor z @ symbolem",
    "A",
    "",
])
def test_author_name_invalid(invalid_author):
    with pytest.raises(ValueError, match="Invalid author name."):
        Book(name="Valid Title", author=invalid_author, year_published=2000, book_type="Fiction")


@pytest.mark.parametrize("malicious_author", [
    "<script>alert('XSS')</script>",
    "Author Name <img src=x onerror=alert(1)>",
    "' OR 1=1 --"
])
def test_author_name_security_rejected(malicious_author):
    with pytest.raises(ValueError, match="Invalid author name."):
        Book(name="Valid Title", author=malicious_author, year_published=2000, book_type="Fiction")