def validate_text(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Text cannot be empty")

    if "<" in value or ">" in value:
        raise ValueError("HTML tags are not allowed")

    return value.strip()
