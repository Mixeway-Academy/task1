import re
from datetime import date


class ValidationError(ValueError):
    """Raised when input data does not meet the domain rules."""


TITLE_PATTERN = re.compile(r"^[\w .,:;!?'()\-]+$")
PERSON_NAME_PATTERN = re.compile(r"^(?:[^\W\d_]|[ .'\-])+$")
CITY_PATTERN = re.compile(r"^(?:[^\W\d_]|[ \-])+$")


def validate_text(value, field, pattern, max_length=64):
    if not isinstance(value, str):
        raise ValidationError(f"{field} must be a text")
    value = value.strip()
    if not 1 <= len(value) <= max_length:
        raise ValidationError(f"{field} must be between 1 and {max_length} characters long")
    if not pattern.fullmatch(value):
        raise ValidationError(f"{field} contains forbidden characters")
    if not re.search(r"[^\W_]", value):
        raise ValidationError(f"{field} must contain at least one letter or digit")
    return value


def validate_int(value, field, min_value, max_value):
    if isinstance(value, bool):
        raise ValidationError(f"{field} must be an integer")
    if isinstance(value, str) and re.fullmatch(r"\s*\d+\s*", value):
        value = int(value)
    if not isinstance(value, int):
        raise ValidationError(f"{field} must be an integer")
    if not min_value <= value <= max_value:
        raise ValidationError(f"{field} must be between {min_value} and {max_value}")
    return value


def validate_choice(value, field, choices):
    if value not in choices:
        raise ValidationError(f"{field} must be one of: {', '.join(choices)}")
    return value


def validate_book_title(value, field="Book name"):
    return validate_text(value, field, TITLE_PATTERN)


def validate_person_name(value, field="Name"):
    return validate_text(value, field, PERSON_NAME_PATTERN)


def validate_city(value, field="City"):
    return validate_text(value, field, CITY_PATTERN)


def validate_year(value, field="Year published"):
    return validate_int(value, field, 1, date.today().year)