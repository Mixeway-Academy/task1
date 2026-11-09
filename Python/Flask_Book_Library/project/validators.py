"""Whitelist input validation for domain objects: invalid values are rejected, not sanitized."""
import re
from datetime import date

# Any unicode letter (no digits, no underscore).
_LETTER = r"[^\W\d_]"

PERSON_NAME_RE = re.compile(rf"{_LETTER}(?:{_LETTER}|[ '\-])*{_LETTER}")
AUTHOR_RE = re.compile(rf"{_LETTER}(?:{_LETTER}|[ '\-.])*(?:{_LETTER}|\.)")
CITY_RE = re.compile(rf"{_LETTER}(?:{_LETTER}|[ '\-.])*{_LETTER}")
BOOK_TITLE_RE = re.compile(rf"(?:{_LETTER}|\d)(?:{_LETTER}|\d|[ .,:;!?'\-()])*")

NAME_MIN_LEN = 2
NAME_MAX_LEN = 64  # matches db.String(64)

BOOK_TYPES = ("2days", "5days", "10days")

MIN_YEAR_PUBLISHED = 1450  # Gutenberg press
MIN_AGE = 1
MAX_AGE = 120


def _validate_text(value, field, pattern, min_len=NAME_MIN_LEN, max_len=NAME_MAX_LEN):
    if not isinstance(value, str):
        raise ValueError(f"{field}: expected text")
    value = value.strip()
    if not min_len <= len(value) <= max_len:
        raise ValueError(f"{field}: length must be between {min_len} and {max_len} characters")
    if "  " in value:
        raise ValueError(f"{field}: consecutive spaces are not allowed")
    if not pattern.fullmatch(value):
        raise ValueError(f"{field}: contains characters that are not allowed")
    return value


def _validate_int(value, field, min_value, max_value):
    # bool is a subclass of int - reject it explicitly
    if isinstance(value, bool):
        raise ValueError(f"{field}: expected an integer")
    if isinstance(value, str):
        value = value.strip()
        if not re.fullmatch(r"\d{1,4}", value):
            raise ValueError(f"{field}: expected an integer")
        value = int(value)
    if not isinstance(value, int):
        raise ValueError(f"{field}: expected an integer")
    if not min_value <= value <= max_value:
        raise ValueError(f"{field}: must be between {min_value} and {max_value}")
    return value


def validate_person_name(value, field="name"):
    return _validate_text(value, field, PERSON_NAME_RE)


def validate_author(value, field="author"):
    return _validate_text(value, field, AUTHOR_RE)


def validate_city(value, field="city"):
    return _validate_text(value, field, CITY_RE)


def validate_book_title(value, field="name"):
    return _validate_text(value, field, BOOK_TITLE_RE, min_len=1)


def validate_book_type(value, field="book_type"):
    if value not in BOOK_TYPES:
        raise ValueError(f"{field}: must be one of {', '.join(BOOK_TYPES)}")
    return value


def validate_year_published(value, field="year_published"):
    return _validate_int(value, field, MIN_YEAR_PUBLISHED, date.today().year)


def validate_age(value, field="age"):
    return _validate_int(value, field, MIN_AGE, MAX_AGE)
