
import pytest
from project.validators.text_validator import validate_text


@pytest.mark.parametrize("value", [
    "The Witcher",
    "George R. R. Martin",
    "Book 123",
    "A normal book title!",
    "",
    None
])
def test_validate_text_accepts_valid_input(value):
    assert validate_text(value) == value


@pytest.mark.parametrize("value", [
    "<script>alert(1)</script>",
    "<img src=x onerror=alert(1)>",
    "<b>Book</b>",
    "javascript:alert(1)",
    "Hello onclick=alert(1)",
    "<SCRIPT>alert(1)</SCRIPT>",
    "<iframe src='example.com'></iframe>"
])
def test_validate_text_rejects_invalid_input(value):
    with pytest.raises(ValueError):
        validate_text(value)


@pytest.mark.parametrize("value", [
    123,
    12.5,
    True,
    []
])
def test_validate_text_rejects_non_string_input(value):
    with pytest.raises(ValueError):
        validate_text(value)
