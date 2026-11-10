import pytest
from project.models import Customer


def test_valid_customer():
    customer = Customer("Jan Kowalski", "Warszawa", 25)

    assert customer.name == "Jan Kowalski"
    assert customer.city == "Warszawa"
    assert customer.age == 25


def test_xss_in_name():
    with pytest.raises(ValueError):
        Customer("<script>alert('XSS')</script>", "Warszawa", 25)


def test_xss_in_city():
    with pytest.raises(ValueError):
        Customer("Jan Kowalski", "<script>alert('XSS')</script>", 25)


def test_empty_name():
    with pytest.raises(ValueError):
        Customer("", "Warszawa", 25)


def test_invalid_age():
    with pytest.raises(ValueError):
        Customer("Jan Kowalski", "Warszawa", "abc")


def test_underage_customer():
    with pytest.raises(ValueError):
        Customer("Jan Kowalski", "Warszawa", 17)


def test_age_over_limit():
    with pytest.raises(ValueError):
        Customer("Jan Kowalski", "Warszawa", 150)


def test_too_long_city():
    with pytest.raises(ValueError):
        Customer("Jan Kowalski", "A" * 65, 25)
