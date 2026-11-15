import re

_TEXT_RE = re.compile(r"^[\w\s.,:;!?()\-]+$", re.UNICODE)
_TITLE_RE = re.compile(r"^[\w\s.,:;!?()\-'’&]+$", re.UNICODE)
VALID_BOOK_TYPES = {"2days", "5days", "10days"}


def _validate(value, field, regex, max_len):
    if not isinstance(value, str):
        raise ValueError(f"{field}: the value must be text")
    value = value.strip()
    if not value:
        raise ValueError(f"{field}: the field cannot be empty")
    if len(value) > max_len:
        raise ValueError(f"{field}: maximum of {max_len} characters")
    if not regex.match(value):
        raise ValueError(f"{field}: prohibited characters")
    return value


def validate_text(value, field, max_len=64):
    return _validate(value, field, _TEXT_RE, max_len)


def validate_title(value, field, max_len=64):
    return _validate(value, field, _TITLE_RE, max_len)


def validate_year(value):
    try:
        year = int(value)
    except (TypeError, ValueError):
        raise ValueError("Year Published: must be a number")
    if not 1000 <= year <= 2100:
        raise ValueError("Year Published: outside the 1000–2100 range")
    return year


def validate_age(value):
    try:
        age = int(value)
    except (TypeError, ValueError):
        raise ValueError("Age: must be a number")
    if not 0 <= age <= 150:
        raise ValueError("Age:  outside the 0–150 range")
    return age


def validate_book_type(value):
    if value not in VALID_BOOK_TYPES:
        raise ValueError("Type: invalid value")
    return value