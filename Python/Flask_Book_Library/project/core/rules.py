import re

class DomainValidationError(ValueError):
    def __init__(self, message, field=None):
        super().__init__(message + f" in field {field}")
        self.field = field

def WordCountBetween(message, min_value, max_value, field=None):
        if message is None:
            msg = f"Text must be between {min_value} and {max_value} characters"
            raise DomainValidationError(msg, field)
        length = len(message)
        if length < min_value or length > max_value:
            msg = message or f"text must be between {min_value} and {max_value} characters"
            raise DomainValidationError(msg, field)
        return True

def OnlyTextRegex(message, field=None):
    compiled = re.compile(r'^[A-Za-z ]+$')
    if not isinstance(message, str):
        msg = message or "Value must be a string"
        raise DomainValidationError(msg, field=field)

    if not compiled.match(message):
        msg = message or "Invalid characters"
        raise DomainValidationError(msg, field=field)
    return True
