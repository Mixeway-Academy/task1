"""Input validation tests for the Book and Customer models (stored XSS).
"""
import pytest

from project.books.models import Book
from project.customers.models import Customer

PAYLOADS_XSS = [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert('XSS')>",
    "\"><script>alert(1)</script>",
    "<svg/onload=alert(1)>",
]


def make_book(**overrides):
    data = {
        'name': 'Wiedźmin',
        'author': 'Andrzej Sapkowski',
        'year_published': 1990,
        'book_type': '2days',
    }
    data.update(overrides)
    return Book(**data)


def make_customer(**overrides):
    data = {'name': 'Jan Kowalski', 'city': 'Warszawa', 'age': 30}
    data.update(overrides)
    return Customer(**data)


# Book
@pytest.mark.parametrize('payload', PAYLOADS_XSS)
def test_book_name_rejects_xss_payload(payload):
    with pytest.raises(ValueError):
        make_book(name=payload)


@pytest.mark.parametrize('payload', PAYLOADS_XSS)
def test_book_author_rejects_xss_payload(payload):
    with pytest.raises(ValueError):
        make_book(author=payload)


def test_book_accepts_valid_data():
    book = make_book()
    assert book.name == 'Wiedźmin'
    assert book.author == 'Andrzej Sapkowski'


def test_book_edit_path_is_validated():
    """Edit assigns attributes directly, bypassing __init__."""
    book = make_book()
    with pytest.raises(ValueError):
        book.name = "<script>alert('XSS')</script>"
    assert book.name == 'Wiedźmin'


# Customer 
@pytest.mark.parametrize('payload', PAYLOADS_XSS)
def test_customer_name_rejects_xss_payload(payload):
    with pytest.raises(ValueError):
        make_customer(name=payload)


@pytest.mark.parametrize('payload', PAYLOADS_XSS)
def test_customer_city_rejects_xss_payload(payload):
    with pytest.raises(ValueError):
        make_customer(city=payload)


def test_customer_accepts_valid_data():
    customer = make_customer()
    assert customer.name == 'Jan Kowalski'
    assert customer.city == 'Warszawa'


def test_customer_edit_path_is_validated():
    customer = make_customer()
    with pytest.raises(ValueError):
        customer.city = "<img src=x onerror=alert(1)>"
    assert customer.city == 'Warszawa'
