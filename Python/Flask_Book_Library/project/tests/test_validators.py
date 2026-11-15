import pytest
from project.validators import (
    validate_text, validate_title, validate_year, validate_age, validate_book_type,
)


@pytest.mark.parametrize("title", [
    "Pan Tadeusz", "1984", "Fahrenheit 451", "Lalka (tom 1)", "Żółć", "Dune: Messiah",
])
def test_title_valid(title):
    assert validate_title(title, "name") == title


@pytest.mark.parametrize("title", ["Harry Potter's Quest", "Pride & Prejudice"])
def test_title_allows_apostrophe_and_ampersand(title):
    assert validate_title(title, "name") == title


@pytest.mark.parametrize("payload", [
    "<script>alert(1)</script>",
    "<img src=x onerror=alert('XSS')>",
    "<svg/onload=alert(1)>",
    '" onmouseover="alert(1)',
    "<b>bold</b>",
])
def test_title_rejects_xss_payloads(payload):
    with pytest.raises(ValueError):
        validate_title(payload, "name")


@pytest.mark.parametrize("value", ["", "   ", "\t\n"])
def test_title_rejects_empty(value):
    with pytest.raises(ValueError):
        validate_title(value, "name")


def test_title_length_limit():
    assert validate_title("a" * 64, "name") == "a" * 64
    with pytest.raises(ValueError):
        validate_title("a" * 65, "name")


@pytest.mark.parametrize("value", [None, 123, [], {"a": 1}])
def test_text_rejects_non_string(value):
    with pytest.raises(ValueError):
        validate_text(value, "author")


def test_text_strips_whitespace():
    assert validate_text("  Henryk Sienkiewicz  ", "author") == "Henryk Sienkiewicz"


def test_text_stricter_than_title():
    assert validate_title("Tom & Jerry", "name") == "Tom & Jerry"
    with pytest.raises(ValueError):
        validate_text("Tom & Jerry", "author")


@pytest.mark.parametrize("value, expected", [("2020", 2020), (1999, 1999), ("1000", 1000), ("2100", 2100)])
def test_year_valid(value, expected):
    assert validate_year(value) == expected


@pytest.mark.parametrize("value", ["abc", "20.5", None, "999", "2101", "<script>"])
def test_year_invalid(value):
    with pytest.raises(ValueError):
        validate_year(value)


@pytest.mark.parametrize("value", ["2days", "5days", "10days"])
def test_book_type_valid(value):
    assert validate_book_type(value) == value


@pytest.mark.parametrize("value", ["3days", "", None, "<script>"])
def test_book_type_invalid(value):
    with pytest.raises(ValueError):
        validate_book_type(value)


def test_age_range():
    assert validate_age("0") == 0
    assert validate_age(150) == 150
    for bad in (-1, 151, "x", None):
        with pytest.raises(ValueError):
            validate_age(bad)