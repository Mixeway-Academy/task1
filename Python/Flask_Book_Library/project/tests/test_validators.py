import pytest

from project.books.models import Book

FIELDS = ["name", "author"]

VALID = {
    "name": "Wiedźmin",
    "author": "Andrzej Sapkowski",
    "year_published": 1990,
    "book_type": "fantasy",
    "status": "available",
}


def make(**overrides):
    """Tworzy obiekt z poprawnych danych, podmieniając wskazane pola."""
    return Book(**{**VALID, **overrides})


XSS_PAYLOADS = [
    "<script>alert('XSS')</script>",
    "<script>alert(1)</script>",
    "<img src=x onerror=alert(1)>",
    "<svg onload=alert(1)>",
    '" onmouseover="alert(1)',
    "'><script>alert(1)</script>",
    "<b>pogrubione</b>",
]


@pytest.mark.parametrize("field", FIELDS)
@pytest.mark.parametrize("payload", XSS_PAYLOADS)
def test_rejects_xss_payloads(field, payload):
    with pytest.raises(ValueError):
        make(**{field: payload})


@pytest.mark.parametrize("field", FIELDS)
@pytest.mark.parametrize("char", list("<>\"'`&/\\{};="))
def test_rejects_each_forbidden_char(field, char):
    with pytest.raises(ValueError):
        make(**{field: f"Tytul{char}test"})


@pytest.mark.parametrize("field", FIELDS)
def test_rejects_too_long_value(field):
    with pytest.raises(ValueError):
        make(**{field: "a" * 1000})