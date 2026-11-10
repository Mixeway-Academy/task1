import pytest
from project.customers.models import Customer


def create_customer(name="Jan Kowalski", city="Warszawa", age=30):
    return Customer(name=name, city=city, age=age)


# Valid test cases for Customer model
def test_create_customer_valid():
    customer = create_customer()
    assert customer.name == "Jan Kowalski"
    assert customer.city == "Warszawa"
    assert customer.age == 30


# XSS test cases for each customer field
@pytest.mark.parametrize(
    "field, value",
    [
        ("name", "<script>alert('XSS')</script>"),
        ("city", "<script>alert('XSS')</script>"),
    ],
)
def test_create_customer_xss(field, value):
    with pytest.raises(ValueError) as excinfo:
        kwargs = {}
        kwargs[field] = value
        create_customer(**kwargs)
    assert "Input contains invalid characters." in str(excinfo.value)
