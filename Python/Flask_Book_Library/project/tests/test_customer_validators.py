import pytest

from project.customers.models import Customer

FIELDS = ["name", "city"]

VALID = {
    "name": "Jan Kowalski",
    "city": "Kraków",
    "age": 30,
}

XSS_PAYLOADS = [
    "<script>alert('XSS')</script>",
    "<script>alert(1)</script>",
    "<img src=x onerror=alert(1)>",
    "<svg onload=alert(1)>",
    '" onmouseover="alert(1)',
    "'><script>alert(1)</script>",
    "<b>pogrubione</b>",
]


def make(**overrides):
    return Customer(**{**VALID, **overrides})


@pytest.mark.parametrize("field", FIELDS)
@pytest.mark.parametrize("payload", XSS_PAYLOADS)
def test_rejects_xss_payloads(field, payload):
    with pytest.raises(ValueError):
        make(**{field: payload})


@pytest.mark.parametrize("field", FIELDS)
@pytest.mark.parametrize("char", list("<>\"'`&/\\{};="))
def test_rejects_each_forbidden_char(field, char):
    with pytest.raises(ValueError):
        make(**{field: f"Tekst{char}test"})


@pytest.mark.parametrize("field", FIELDS)
@pytest.mark.parametrize("value", ["", "   ", None])
def test_rejects_empty_values(field, value):
    with pytest.raises(ValueError):
        make(**{field: value})


@pytest.mark.parametrize("field", FIELDS)
def test_rejects_too_long_value(field):
    with pytest.raises(ValueError):
        make(**{field: "a" * 1000})


@pytest.mark.parametrize("field", FIELDS)
@pytest.mark.parametrize("value", ["Jan Kowalski", "Łódź, miasto kontrastów"])
def test_accepts_valid_values(field, value):
    customer = make(**{field: value})
    assert getattr(customer, field) == value


@pytest.mark.parametrize("field", FIELDS)
def test_strips_surrounding_whitespace(field):
    customer = make(**{field: "  Jan Kowalski  "})
    assert getattr(customer, field) == "Jan Kowalski"