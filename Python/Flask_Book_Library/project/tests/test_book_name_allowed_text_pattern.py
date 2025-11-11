import re

BOOK_NAME_ALLOWED_TEXT_PATTERN = re.compile(r"^[A-Za-z0-9À-ž\s\.\,\-']+$")

test_cases = [
    ("Władca pierścienie", True),
    ("Mały Ksiąe", True),
    ("Cien años de soledad", True),
    ("1984", True),
    ("<script>alert('Atak')</script>", False),
    ("", False),
]

for book_name, expected in test_cases:
    match = bool(BOOK_NAME_ALLOWED_TEXT_PATTERN.match(book_name))
    assert match == expected, f"Failed for book_name: '{book_name}'"

print("All tests passed!")