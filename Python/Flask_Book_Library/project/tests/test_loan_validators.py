from datetime import datetime

import pytest

from project.loans.models import Loan

FIELDS = [
    "customer_name",
    "book_name",
    "original_author",
    "original_book_type",
]

VALID = {
    "customer_name": "Jan Kowalski",
    "book_name": "Wiedźmin",
    "loan_date": datetime(2026, 1, 1),
    "return_date": datetime(2026, 1, 10),
    "original_author": "Andrzej Sapkowski",
    "original_year_published": 1990,
    "original_book_type": "fantasy",
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
    return Loan(**{**VALID, **overrides})


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
def test_rejects_too_long_value(field):
    with pytest.raises(ValueError):
        make(**{field: "a" * 1000})
