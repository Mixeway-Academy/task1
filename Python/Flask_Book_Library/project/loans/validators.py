from datetime import date, datetime

from project.books.validators import (
    ValidationError,
    validate_author,
    validate_book_type,
    validate_name,
    validate_year_published,
)
from project.customers.validators import validate_customer_name


MIN_YEAR = 1900
MAX_YEAR = 2100


def _labelled(validator, label):
    def wrapper(value):
        try:
            return validator(value)
        except ValidationError as e:
            raise ValidationError(f"{label}: {e}") from None
    return wrapper


def _as_date(value, field):
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    raise ValidationError(f"{field} must be a date")


def _validate_date(value, field):
    day = _as_date(value, field)
    if not MIN_YEAR <= day.year <= MAX_YEAR:
        raise ValidationError(f"{field} year must be between {MIN_YEAR} and {MAX_YEAR}")
    return value


def validate_loan_date(value):
    return _validate_date(value, 'loan_date')


def validate_return_date(value):
    return _validate_date(value, 'return_date')


def validate_loan_period(loan_date, return_date):
    if _as_date(return_date, 'return_date') < _as_date(loan_date, 'loan_date'):
        raise ValidationError("return_date must not be earlier than loan_date")


LOAN_VALIDATORS = {
    'customer_name': _labelled(validate_customer_name, 'customer_name'),
    'book_name': _labelled(validate_name, 'book_name'),
    'loan_date': validate_loan_date,
    'return_date': validate_return_date,
    'original_author': _labelled(validate_author, 'original_author'),
    'original_year_published': _labelled(validate_year_published, 'original_year_published'),
    'original_book_type': _labelled(validate_book_type, 'original_book_type'),
}