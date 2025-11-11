# test_validate_book_name.py
import pytest
from project.books.validators import validate_book_name
@pytest.mark.parametrize("valid_name", [
    "Adam Mickiewicz",
    "Szryja",
    "Book2025",
    "Title 999 1111111111"
])
def test_valid_names(valid_name):
    """Sprawdza poprawne nazwy książek (litery i cyfry)"""
    assert validate_book_name(valid_name)

@pytest.mark.parametrize("invalid_name", [
    "",
    "Book@2025",
    "<script>alert(1)</script>"
    "<img src=x onerror=alert(1)>",
    "Hello<script>",
    "drop table users;",
    "name;alert(1)",
    "javascript:alert(1)"
])
def test_invalid_names(invalid_name):
    """Sprawdza niepoprawne nazwy książek (potencjalny XSS i inne znaki)"""
    assert not validate_book_name(invalid_name)
