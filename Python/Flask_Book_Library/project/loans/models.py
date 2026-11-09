from datetime import date, datetime

from sqlalchemy.orm import validates

from project import db, app
from project.validators import (
  ValidationError,
  validate_book_title,
  validate_person_name,
  validate_year,
  validate_choice,
)
from project.books.models import BOOK_TYPES


def _as_date(value):
    return value.date() if isinstance(value, datetime) else value

# Loan model
class Loan(db.Model):
    __tablename__ = 'Loans'

    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(64), nullable=False)
    book_name = db.Column(db.String(64), nullable=False)
    loan_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime, nullable=False)
    original_author = db.Column(db.String(64), nullable=False)
    original_year_published = db.Column(db.Integer, nullable=False)
    original_book_type = db.Column(db.String(64), nullable=False)

    def __init__(self, customer_name, book_name, loan_date, return_date, original_author, original_year_published, original_book_type):
        self.customer_name = customer_name
        self.book_name = book_name
        self.loan_date = loan_date
        self.return_date = return_date
        self.original_author = original_author
        self.original_year_published = original_year_published
        self.original_book_type = original_book_type

    @validates('customer_name')
    def validate_customer_name(self, key, value):
        return validate_person_name(value, 'Customer name')

    @validates('book_name')
    def validate_book_name(self, key, value):
        return validate_book_title(value, 'Book name')

    @validates('loan_date')
    def validate_loan_date(self, key, value):
        if not isinstance(value, date):
            raise ValidationError('Loan date must be a valid date')
        return value

    @validates('return_date')
    def validate_return_date(self, key, value):
        if not isinstance(value, date):
            raise ValidationError('Return date must be a valid date')
        if self.loan_date is not None and _as_date(value) < _as_date(self.loan_date):
            raise ValidationError('Return date cannot be earlier than loan date')
        return value

    @validates('original_author')
    def validate_original_author(self, key, value):
        return validate_person_name(value, 'Author')

    @validates('original_year_published')
    def validate_original_year_published(self, key, value):
        return validate_year(value, 'Year published')

    @validates('original_book_type')
    def validate_original_book_type(self, key, value):
        return validate_choice(value, 'Book type', BOOK_TYPES)

    def __repr__(self):
        return f"Customer: {self.customer_name}, Book: {self.book_name}, Loan Date: {self.loan_date}, Return Date: {self.return_date}"


with app.app_context():
    db.create_all()