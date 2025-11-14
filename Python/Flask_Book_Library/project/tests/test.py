import re
REGEX_PATTERN_AUTHOR_NAME = r"^[A-Za-z0-9À-ž\s\.\,\-']+$"
AUTHOR_NAME_RE = re.compile(REGEX_PATTERN_AUTHOR_NAME)
tests = [
    ("J. K. Rowling", True),
    ("Robert Lewandowski", True),
    ("<script>alert('test')</script>", False),
    ("", False),
]

for author_name, expected in tests:
    match = bool(AUTHOR_NAME_RE.fullmatch(author_name))
    assert match == expected, f"Test for: '{author_name}' failed. Expected {expected}, got {match}"