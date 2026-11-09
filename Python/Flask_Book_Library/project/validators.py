def validate(value):
    if '<' in str(value) or '>' in str(value):
        raise ValueError("Forbidden characters")
    return value
