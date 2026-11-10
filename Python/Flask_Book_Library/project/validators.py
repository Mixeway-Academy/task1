"""Input validation shared by the models (protection against stored XSS).
"""
import re

MAX_TEXT_LENGTH = 64  # matches db.String(64) columns

# Letters (incl. Polish diacritics), digits, spaces and basic punctuation.
TEXT_PATTERN = re.compile(r"[\w .,:;!?'()\-]+")


def validate_text(value, field):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'{field} must be a non-empty text.')
    value = value.strip()
    if len(value) > MAX_TEXT_LENGTH:
        raise ValueError(f'{field} must be at most {MAX_TEXT_LENGTH} characters long.')
    # fullmatch, not match with ^...$ - "$" also matches before a trailing "\n".
    if not TEXT_PATTERN.fullmatch(value):
        raise ValueError(f'{field} contains forbidden characters.')
    return value


def validate_number(value, field):
    if isinstance(value, str) and value.strip().isdecimal():
        return int(value)
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    raise ValueError(f'{field} must be a number.')


def validate_choice(value, field, choices):
    if value not in choices:
        raise ValueError(f'{field} must be one of: {", ".join(choices)}.')
    return value
