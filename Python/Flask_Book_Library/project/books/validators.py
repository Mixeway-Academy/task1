import re

def validate_book_name(name):
    return re.match(r'^[A-Za-z0-9 ]+$', name)