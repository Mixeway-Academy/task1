from unicodedata import category


def validate_text(field, value):
    if not isinstance(value, str) or not value.strip() or len(value) > 64:
        raise ValueError(f'{field} must contain 1-64 characters of text.')
    if any(char in '<>' or category(char) == 'Cc' for char in value):
        raise ValueError(f'{field} must not contain HTML or control characters.')
    return value
