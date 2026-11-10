"""
Walidacja danych wejściowych na poziomie tworzenia/modyfikacji obiektów modeli.

Wszystkie pola tekstowe przechodzą przez ``validate_text``. Stosowana jest
biała lista znaków: litery (również polskie i inne znaki Unicode), cyfry,
spacja oraz bezpieczna interpunkcja. Znaki potrzebne do wstrzyknięcia kodu
HTML/JavaScript (m.in. ``< > " ` / \\ = { }``) są odrzucane, więc złośliwy
payload nigdy nie trafia do bazy danych.
"""
import re

MAX_TEXT_LENGTH = 64

# \w w Pythonie 3 obejmuje litery Unicode (ą, ę, ł, ...), cyfry i "_"
_ALLOWED_TEXT = re.compile(r"^[\w .,'\-:;!?()&]+$")

ALLOWED_BOOK_TYPES = ("2days", "5days", "10days")


def validate_text(field, value, max_length=MAX_TEXT_LENGTH, required=True):
    """Zwraca oczyszczoną wartość albo rzuca ValueError."""
    if not required and (value is None or (isinstance(value, str) and not value.strip())):
        return ""
    if not isinstance(value, str):
        raise ValueError(f"{field}: wartość musi być tekstem")

    value = value.strip()

    if not value:
        raise ValueError(f"{field}: pole nie może być puste")
    if len(value) > max_length:
        raise ValueError(f"{field}: maksymalna długość to {max_length} znaków")
    if not _ALLOWED_TEXT.fullmatch(value):
        raise ValueError(f"{field}: pole zawiera niedozwolone znaki")

    return value


def validate_book_type(field, value):
    if value not in ALLOWED_BOOK_TYPES:
        raise ValueError(f"{field}: dozwolone wartości to {', '.join(ALLOWED_BOOK_TYPES)}")
    return value
