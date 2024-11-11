from pydantic import BaseModel, Field, constr, conint, condate, validate_arguments
from typing import Literal

CITY_NAME_REGEX = "^[A-Z\u0080-\u024F][a-zA-Z\u0080-\u024F]*(?:[.\-'\s][a-zA-Z\u0080-\u024F]+)*$" # regex from https://stackoverflow.com/questions/11757013/regular-expressions-for-city-name
BOOK_NAME_REGEX = "^[A-Za-z0-9\s\-_,\.;:()!'\"]+$" # regex from https://stackoverflow.com/questions/17721013/regular-expression-for-matching-titles-ex-book-title
PERSON_NAME_REGEX = "^[A-Z\u0100-\u017F][a-zA-Z\u0100-\u017F '.-]*[A-Za-z\u0100-\u017F][^-]$" # regex from https://stackoverflow.com/questions/2385701/regular-expression-for-first-and-last-name

book_name = Field(pattern=BOOK_NAME_REGEX, strip_whitespace=True, min_length=1, max_length=64)
person_name = Field(pattern=PERSON_NAME_REGEX, strip_whitespace=True, min_length=2, max_length=64)
city_name = Field(pattern=CITY_NAME_REGEX, strip_whitespace=True, min_length=3, max_length=64)
age = Field(gt=0)

class CustomerModel(BaseModel):
    name: str = person_name
    city: str = city_name
    age: int = age

def validate_customer_model(name, city, age):
    return CustomerModel(
        name=name,
        city=city,
        age=age,
    ).dict()


class BookModel(BaseModel):
    name: str = book_name
    author: str = person_name
    year_published: int = age
    book_type: Literal['2days', '5days', '10days']

def validate_book_model(name, author, year_published, book_type):
    return BookModel(
        name=name,
        author=author,
        year_published=year_published,
        book_type=book_type
    ).dict()

class LoanModel(BaseModel):
    customer_name: str = person_name
    book_name: str = book_name
    loan_date: condate()
    return_date: condate()
    original_author: str = person_name
    original_year_published: int = age
    original_book_type: Literal['2days', '5days', '10days']
