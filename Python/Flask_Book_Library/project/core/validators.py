XSS_CHARS = ["<", ">", '"', "'", "/", "\\", "&"]


def validate_text(value):
    if any(char in value for char in XSS_CHARS):
        raise ValueError("Input contains invalid characters.")
    return value
