import re


def validate_text(value, field_name, max_length=64):
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    
    value = value.strip()
    
    if not value:
        raise ValueError(f"{field_name} cannot be empty")
    
    if len(value) > 64:
        raise ValueError(f"{field_name} cannot be longer than 64 characters")
    
    if re.search(r'[<>]', value):
        raise ValueError(f"{field_name} cannot contain special characters like [,],<,>")
    
    return value