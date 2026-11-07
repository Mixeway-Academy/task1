import re


def validate_text(value):
    if value is None:
        return value

    if not isinstance(value, str):
        raise ValueError("Value must be a string")

    forbidden_patterns = [
        r"<[^>]*>",
        r"javascript\s*:",
        r"on\w+\s*="
    ]

    for pattern in forbidden_patterns:
        if re.search(pattern, value, re.IGNORECASE):
            raise ValueError("Invalid characters or HTML content detected")

    return value
