import re
import unicodedata
from datetime import date


class ValidationError(ValueError):
    """Raised when a Book field does not satisfy the validation rules."""

BOOK_TYPES = ('2days', '5days', '10days')
BOOK_STATUSES = ('available', 'loaned')

NAME_MAX_LENGTH = 64
AUTHOR_MAX_LENGTH = 64
MIN_YEAR = 1

_NAME_PATTERN = re.compile(r"[\w .,:;!?'’\"“”„&()\-–—/#+]+")

_ENTITY_PATTERN = re.compile(r"&#?\w+;")

_AUTHOR_PATTERN = re.compile(r"(?:[^\W\d_]|[ .,'’\-])+")

_YEAR_PATTERN = re.compile(r"[0-9]{1,4}")


def _clean_text(value, field, max_length, pattern):
    if value is None:
        raise ValidationError(f"{field} is required")
    if not isinstance(value, str):
        raise ValidationError(f"{field} must be a string")

    value = unicodedata.normalize('NFC', value)
    value = ' '.join(value.split())

    if not value:
        raise ValidationError(f"{field} is required")
    if len(value) > max_length:
        raise ValidationError(f"{field} must be at most {max_length} characters long")
    if not pattern.fullmatch(value):
        raise ValidationError(f"{field} contains forbidden characters")
    return value


def validate_name(value):
    value = _clean_text(value, 'name', NAME_MAX_LENGTH, _NAME_PATTERN)
    if _ENTITY_PATTERN.search(value):
        raise ValidationError("name contains forbidden characters")
    if not any(ch.isalnum() for ch in value):
        raise ValidationError("name must contain at least one letter or digit")
    return value


def validate_author(value):
    value = _clean_text(value, 'author', AUTHOR_MAX_LENGTH, _AUTHOR_PATTERN)
    if not any(ch.isalpha() for ch in value):
        raise ValidationError("author must contain at least one letter")
    return value


def validate_year_published(value):
    if value is None or isinstance(value, bool):
        raise ValidationError("year_published must be an integer year")

    if isinstance(value, str):
        value = value.strip()
        if not _YEAR_PATTERN.fullmatch(value):
            raise ValidationError("year_published must be an integer year")
        value = int(value)
    elif not isinstance(value, int):
        raise ValidationError("year_published must be an integer year")

    max_year = date.today().year
    if not MIN_YEAR <= value <= max_year:
        raise ValidationError(f"year_published must be between {MIN_YEAR} and {max_year}")
    return value


def _validate_choice(value, field, allowed):
    if not isinstance(value, str) or value.strip() not in allowed:
        raise ValidationError(f"{field} must be one of: {', '.join(allowed)}")
    return value.strip()


def validate_book_type(value):
    return _validate_choice(value, 'book_type', BOOK_TYPES)


def validate_status(value):
    return _validate_choice(value, 'status', BOOK_STATUSES)


BOOK_VALIDATORS = {
    'name': validate_name,
    'author': validate_author,
    'year_published': validate_year_published,
    'book_type': validate_book_type,
    'status': validate_status,
}