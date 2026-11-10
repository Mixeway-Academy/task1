def validate_text(field, value, optional=False):
    if optional and value is None:
        return value
    if not isinstance(value, str) or '<' in value or '>' in value:
        raise ValueError(f'{field} must be plain text without angle brackets')
    if len(value) > 64:
        raise ValueError(f'{field} must be at most 64 characters long')
    if not optional and not value.strip():
        raise ValueError(f'{field} must not be blank')
    return value
