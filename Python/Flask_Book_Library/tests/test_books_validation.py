import pytest
from project.books.models import Book


@pytest.fixture
def sut():
    return Book('name', 'author', 2000, '2days')


@pytest.mark.parametrize('valid_name', [
    'A',
    'a',
    '1',
    'A really long book name - read it yourself!',
])
def test_valid_name(sut: Book, valid_name: str):
    sut.validate_name('name', valid_name)

@pytest.mark.parametrize('invalid_name', [
    '<script>alert(1)</script>',
    '()[]{}',
    '~~~~',
])
def test_invalid_name(sut: Book, invalid_name: str):
    with pytest.raises(ValueError):
        sut.validate_name('name', invalid_name)


@pytest.mark.parametrize('valid_author', [
    'A',
    'a',
    'Georgia O\'Keeffe',
])
def test_valid_author(sut: Book, valid_author: str):
    sut.validate_author('author', valid_author)

@pytest.mark.parametrize('invalid_author', [
    '<script>alert(1)</script>',
    '()[]{}',
    '1',
    '~~~~',
])
def test_invalid_author(sut: Book, invalid_author: str):
    with pytest.raises(ValueError):
        sut.validate_author('author', invalid_author)


@pytest.mark.parametrize('valid_year_published', [
    500,
    2500,
    1000,
    1234,
])
def test_valid_year_published(sut: Book, valid_year_published: str):
    sut.validate_year_published('year_published', valid_year_published)

@pytest.mark.parametrize('invalid_year_published', [
    '<script>alert(1)</script>',
    '()[]{}',
    '~~~~',
    -100,
    0,
    3000,
])
def test_invalid_year_published(sut: Book, invalid_year_published: str):
    with pytest.raises(ValueError):
        sut.validate_year_published('year_published', invalid_year_published)


@pytest.mark.parametrize('valid_book_type', [
    '2days',
    '5days',
    '10days',
])
def test_valid_book_type(sut: Book, valid_book_type: str):
    sut.validate_book_type('book_type', valid_book_type)

@pytest.mark.parametrize('invalid_book_type', [
    '1day',
    '7days',
    '<script>alert(1)</script>',
    '()[]{}',
    '~~~~',
])
def test_invalid_book_type(sut: Book, invalid_book_type: str):
    with pytest.raises(ValueError):
        sut.validate_book_type('book_type', invalid_book_type)
