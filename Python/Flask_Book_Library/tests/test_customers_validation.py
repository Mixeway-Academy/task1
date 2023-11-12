import pytest
from project.customers.models import Customer


@pytest.fixture
def sut():
    return Customer('name', 'city', 20)


@pytest.mark.parametrize('valid_name', [
    'A',
    'a',
    'Ala Ma-Kota',
    'Georgia O\'Keeffe',
])
def test_valid_name(sut: Customer, valid_name: str):
    sut.validate_name('name', valid_name)

@pytest.mark.parametrize('invalid_name', [
    '<script>alert(1)</script>',
    '()[]{}',
    '1',
    '~~~~',
])
def test_invalid_name(sut: Customer, invalid_name: str):
    with pytest.raises(ValueError):
        sut.validate_name('name', invalid_name)


@pytest.mark.parametrize('valid_city', [
    'A',
    'a',
    'O\'Fallon',
])
def test_valid_city(sut: Customer, valid_city: str):
    sut.validate_city('city', valid_city)

@pytest.mark.parametrize('invalid_city', [
    '<script>alert(1)</script>',
    '()[]{}',
    '1',
    '~~~~',
])
def test_invalid_city(sut: Customer, invalid_city: str):
    with pytest.raises(ValueError):
        sut.validate_city('city', invalid_city)


@pytest.mark.parametrize('valid_age', [
    0,
    200,
    5,
    20,
])
def test_valid_age(sut: Customer, valid_age: str):
    sut.validate_age('age', valid_age)

@pytest.mark.parametrize('invalid_age', [
    '<script>alert(1)</script>',
    '()[]{}',
    '~~~~',
    -100,
    3000,
])
def test_invalid_age(sut: Customer, invalid_age: str):
    with pytest.raises(ValueError):
        sut.validate_age('age', invalid_age)
