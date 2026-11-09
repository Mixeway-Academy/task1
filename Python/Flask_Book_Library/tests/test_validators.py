from datetime import date, timedelta

import pytest

from project.validators import ValidationError
from project.books.models import Book
from project.customers.models import Customer
from project.loans.models import Loan


XSS_PAYLOADS = [
  "<script>alert('XSS')</script>",
  '<img src=x onerror="alert(1)">',
  "<svg onload=alert(1)>",
  '"><script>alert(1)</script>',
  "Pan Tadeusz</td><script>alert(1)</script>",
]


def make_book(**overrides):
  data = dict(name="Pan Tadeusz", author="Adam Mickiewicz", year_published=1834, book_type="5days")
  data.update(overrides)
  return Book(**data)


def make_customer(**overrides):
  data = dict(name="Jan Kowalski", city="Kraków", age=30)
  data.update(overrides)
  return Customer(**data)


def make_loan(**overrides):
  data = dict(
      customer_name="Jan Kowalski",
      book_name="Pan Tadeusz",
      loan_date=date(2026, 11, 1),
      return_date=date(2026, 11, 6),
      original_author="Adam Mickiewicz",
      original_year_published=1834,
      original_book_type="5days",
  )
  data.update(overrides)
  return Loan(**data)


# ---------- Book: valid data ----------

def test_valid_book_is_created():
  book = make_book()
  assert book.name == "Pan Tadeusz"
  assert book.author == "Adam Mickiewicz"
  assert book.year_published == 1834
  assert book.status == "available"


@pytest.mark.parametrize("name", ["Ogniem i mieczem, tom 1", "Solaris", "1984", "Kto? Co? (wyd. 2)"])
def test_valid_book_names_are_accepted(name):
  assert make_book(name=name).name == name


@pytest.mark.parametrize("author", ["Stanisław Lem", "J.R.R. Tolkien", "Flannery O'Connor", "Maria Konopnicka-Nowak"])
def test_valid_authors_are_accepted(author):
  assert make_book(author=author).author == author


def test_book_year_given_as_text_is_converted_to_int():
  assert make_book(year_published="1999").year_published == 1999


def test_book_whitespace_is_trimmed():
  assert make_book(name="  Solaris  ").name == "Solaris"


# ---------- Book: invalid data ----------

@pytest.mark.parametrize("field", ["name", "author"])
@pytest.mark.parametrize("payload", XSS_PAYLOADS)
def test_book_rejects_xss(field, payload):
  with pytest.raises(ValidationError):
      make_book(**{field: payload})


@pytest.mark.parametrize("name", ["", "   ", "a" * 65, None, 123, "---"])
def test_book_rejects_invalid_name(name):
  with pytest.raises(ValidationError):
      make_book(name=name)


@pytest.mark.parametrize("year", [0, -5, date.today().year + 1, "abc", "19.5", True, None])
def test_book_rejects_invalid_year(year):
  with pytest.raises(ValidationError):
      make_book(year_published=year)


@pytest.mark.parametrize("book_type", ["7days", "", "<script>alert(1)</script>", None])
def test_book_rejects_invalid_type(book_type):
  with pytest.raises(ValidationError):
      make_book(book_type=book_type)


def test_editing_book_with_xss_is_rejected():
  book = make_book()
  with pytest.raises(ValidationError):
      book.name = "<script>alert('XSS')</script>"
  assert book.name == "Pan Tadeusz"


# ---------- Customer ----------

def test_valid_customer_is_created():
  customer = make_customer()
  assert customer.name == "Jan Kowalski"
  assert customer.city == "Kraków"
  assert customer.age == 30


def test_customer_age_given_as_text_is_converted_to_int():
  assert make_customer(age="42").age == 42


@pytest.mark.parametrize("field", ["name", "city"])
@pytest.mark.parametrize("payload", XSS_PAYLOADS)
def test_customer_rejects_xss(field, payload):
  with pytest.raises(ValidationError):
      make_customer(**{field: payload})


@pytest.mark.parametrize("name", ["", "Jan123", "a" * 65, None])
def test_customer_rejects_invalid_name(name):
  with pytest.raises(ValidationError):
      make_customer(name=name)


@pytest.mark.parametrize("age", [0, 121, -1, "abc", None])
def test_customer_rejects_invalid_age(age):
  with pytest.raises(ValidationError):
      make_customer(age=age)


def test_editing_customer_with_xss_is_rejected():
  customer = make_customer()
  with pytest.raises(ValidationError):
      customer.city = '<img src=x onerror="alert(1)">'
  assert customer.city == "Kraków"


# ---------- Loan ----------

def test_valid_loan_is_created():
  loan = make_loan()
  assert loan.customer_name == "Jan Kowalski"
  assert loan.book_name == "Pan Tadeusz"


def test_loan_can_be_returned_on_the_same_day():
  day = date(2026, 11, 1)
  assert make_loan(loan_date=day, return_date=day).return_date == day


@pytest.mark.parametrize("field", ["customer_name", "book_name"])
@pytest.mark.parametrize("payload", XSS_PAYLOADS)
def test_loan_rejects_xss(field, payload):
  with pytest.raises(ValidationError):
      make_loan(**{field: payload})


def test_loan_rejects_return_date_before_loan_date():
  with pytest.raises(ValidationError):
      make_loan(loan_date=date(2026, 11, 10), return_date=date(2026, 11, 10) - timedelta(days=1))


@pytest.mark.parametrize("field", ["loan_date", "return_date"])
def test_loan_rejects_missing_date(field):
  with pytest.raises(ValidationError):
      make_loan(**{field: None})


