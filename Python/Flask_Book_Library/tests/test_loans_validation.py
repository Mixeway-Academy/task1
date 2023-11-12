import pytest
from project.loans.models import Loan


@pytest.fixture
def sut():
    return Loan('customer name', 'book name', '2020-01-01T12:34:56', '2020-01-03T12:34:56', 'author', 2000, '2days')


@pytest.mark.parametrize('valid_customer_name', [
    'A',
    'a',
    'Ala Ma-Kota',
    'Georgia O\'Keeffe',
])
def test_valid_customer_name(sut: Loan, valid_customer_name: str):
    sut.validate_customer_name('customer_name', valid_customer_name)

@pytest.mark.parametrize('invalid_customer_name', [
    '<script>alert(1)</script>',
    '()[]{}',
    '1',
    '~~~~',
])
def test_invalid_customer_name(sut: Loan, invalid_customer_name: str):
    with pytest.raises(ValueError):
        sut.validate_customer_name('customer_name', invalid_customer_name)


@pytest.mark.parametrize('valid_book_name', [
    'A',
    'a',
    '1',
    'A really long book name - read it yourself!',
])
def test_valid_book_name(sut: Loan, valid_book_name: str):
    sut.validate_book_name('book_name', valid_book_name)

@pytest.mark.parametrize('invalid_book_name', [
    '<script>alert(1)</script>',
    '()[]{}',
    '~~~~',
])
def test_invalid_book_name(sut: Loan, invalid_book_name: str):
    with pytest.raises(ValueError):
        sut.validate_book_name('book_name', invalid_book_name)


@pytest.mark.parametrize('valid_original_author', [
    'A',
    'a',
    'Georgia O\'Keeffe',
])
def test_valid_original_author(sut: Loan, valid_original_author: str):
    sut.validate_original_author('original_author', valid_original_author)

@pytest.mark.parametrize('invalid_original_author', [
    '<script>alert(1)</script>',
    '()[]{}',
    '1',
    '~~~~',
])
def test_invalid_original_author(sut: Loan, invalid_original_author: str):
    with pytest.raises(ValueError):
        sut.validate_original_author('original_author', invalid_original_author)


@pytest.mark.parametrize('valid_original_year_published', [
    500,
    2500,
    1000,
    1234,
])
def test_valid_original_year_published(sut: Loan, valid_original_year_published: str):
    sut.validate_original_year_published('original_year_published', valid_original_year_published)

@pytest.mark.parametrize('invalid_original_year_published', [
    '<script>alert(1)</script>',
    '()[]{}',
    '~~~~',
    -100,
    0,
    3000,
])
def test_invalid_original_year_published(sut: Loan, invalid_original_year_published: str):
    with pytest.raises(ValueError):
        sut.validate_original_year_published('original_year_published', invalid_original_year_published)


@pytest.mark.parametrize('valid_original_book_type', [
    '2days',
    '5days',
    '10days',
])
def test_valid_original_book_type(sut: Loan, valid_original_book_type: str):
    sut.validate_original_book_type('original_book_type', valid_original_book_type)

@pytest.mark.parametrize('invalid_original_book_type', [
    '1day',
    '7days',
    '<script>alert(1)</script>',
    '()[]{}',
    '~~~~',
])
def test_invalid_original_book_type(sut: Loan, invalid_original_book_type: str):
    with pytest.raises(ValueError):
        sut.validate_original_book_type('original_book_type', invalid_original_book_type)
