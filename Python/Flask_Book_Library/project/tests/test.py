import re

BOOK_NAME_ALLOWED_PATTERN = re.compile(r"^[A-Za-z0-9À-ž\s\.\,\-']+$")

tests = [
    ("Pan Tadeusz", True),
    ("Fahrenheit 451", True),
    ("Les Misérables", True),
    ("", False),
]

for book_name, expected in tests:
    match = bool(BOOK_NAME_ALLOWED_PATTERN.match(book_name))
    assert match == expected, f"Test for: '{book_name}' failed. Expected {expected}, got {match}"