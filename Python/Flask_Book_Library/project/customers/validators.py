import re

from project.books.validators import ValidationError, _clean_text


NAME_MAX_LENGTH = 64
CITY_MAX_LENGTH = 64

MIN_AGE = 1
MAX_AGE = 120

_NAME_PATTERN = re.compile(r"(?:[^\W\d_]|[ .,'’\-])+")

_CITY_PATTERN = re.compile(r"(?:[^\W\d_]|[ .,'’\-()])+")

_AGE_PATTERN = re.compile(r"[0-9]{1,3}")


def validate_customer_name(value):
    value = _clean_text(value, 'name', NAME_MAX_LENGTH, _NAME_PATTERN)
    if not any(ch.isalpha() for ch in value):
        raise ValidationError("name must contain at least one letter")
    return value


def validate_city(value):
    value = _clean_text(value, 'city', CITY_MAX_LENGTH, _CITY_PATTERN)
    if not any(ch.isalpha() for ch in value):
        raise ValidationError("city must contain at least one letter")
    return value


def validate_age(value):
    if value is None or isinstance(value, bool):
        raise ValidationError("age must be an integer")

    if isinstance(value, str):
        value = value.strip()
        if not _AGE_PATTERN.fullmatch(value):
            raise ValidationError("age must be an integer")
        value = int(value)
    elif not isinstance(value, int):
        raise ValidationError("age must be an integer")

    if not MIN_AGE <= value <= MAX_AGE:
        raise ValidationError(f"age must be between {MIN_AGE} and {MAX_AGE}")
    return value


CUSTOMER_VALIDATORS = {
    'name': validate_customer_name,
    'city': validate_city,
    'age': validate_age,
}