import pytest
from pydantic import ValidationError

from project.common.form_models import validate_book_model, validate_customer_model

def test_validate_customer_model_valid():
    valid_data = validate_customer_model(
        name="John Doe",
        city="New York",
        age=30
    )
    assert valid_data["name"] == "John Doe"
    assert valid_data["city"] == "New York"
    assert valid_data["age"] == 30

@pytest.mark.parametrize("test_input", ["J", "test", "<script>alert('js')</script>"])
def test_validate_customer_model_invalid_name(test_input):
    with pytest.raises(ValidationError):
        validate_customer_model(name=test_input, city="New York", age=30)

@pytest.mark.parametrize("test_input", ["J", "test", "NY!", "<script>alert('js')</script>"])
def test_validate_customer_model_invalid_city(test_input):
    with pytest.raises(ValidationError):
        validate_customer_model(name="John Doe", city=test_input, age=30)

def test_validate_customer_model_invalid_age():
    with pytest.raises(ValidationError):
        validate_customer_model(name="John Doe", city="New York", age=-1)

def test_validate_book_model_valid():
    valid_data = validate_book_model(
        name="The Great Gatsby",
        author="F. Scott Fitzgerald",
        year_published=1925,
        book_type="2days"
    )
    assert valid_data["name"] == "The Great Gatsby"
    assert valid_data["author"] == "F. Scott Fitzgerald"
    assert valid_data["year_published"] == 1925
    assert valid_data["book_type"] == "2days"

@pytest.mark.parametrize("test_input", ["", "<script>alert('js')</script>"])
def test_validate_book_model_invalid_name(test_input):
    with pytest.raises(ValidationError):
        validate_book_model(
            name=test_input,
            author="Author Name",
            year_published=2000,
            book_type="5days"
        )

@pytest.mark.parametrize("test_input", ["J", "test", "<script>alert('js')</script>"])
def test_validate_book_model_invalid_author(test_input):
    with pytest.raises(ValidationError):
        validate_book_model(
            name="A Valid Book Title",
            author=test_input,
            year_published=2000,
            book_type="5days"
        )

def test_validate_book_model_invalid_year_published():
    with pytest.raises(ValidationError):
        validate_book_model(
            name="A Valid Book Title",
            author="Author Name",
            year_published=-100,
            book_type="10days"
        )

def test_validate_book_model_invalid_book_type():
    with pytest.raises(ValidationError):
        validate_book_model(
            name="A Valid Book Title",
            author="Author Name",
            year_published=2000,
            book_type="7days"
        )
