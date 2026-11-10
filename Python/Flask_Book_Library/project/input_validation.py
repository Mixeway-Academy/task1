"""Reject HTML in fields stored for display as plain text."""

import nh3


def validate_plain_text(field_name, value):
    """Keep ordinary values unchanged and reject HTML markup in strings."""
    if isinstance(value, str) and nh3.is_html(value):
        raise ValueError(f'{field_name} cannot contain HTML markup')
    return value
