from sqlalchemy.orm import validates

from project import db , app
from project.validators import (
    validate_author,
    validate_book_title,
    validate_book_type,
    validate_person_name,
    validate_year_published,
)


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

    # Same rules as Book and Customer (a loan stores copies of their values).
    @validates('customer_name')
    def _check_customer_name(self, key, value):
        return validate_person_name(value, key)

    @validates('book_name')
    def _check_book_name(self, key, value):
        return validate_book_title(value, key)

    @validates('original_author')
    def _check_original_author(self, key, value):
        return validate_author(value, key)

    @validates('original_year_published')
    def _check_original_year_published(self, key, value):
        return validate_year_published(value, key)

    @validates('original_book_type')
    def _check_original_book_type(self, key, value):
        return validate_book_type(value, key)

    def __repr__(self):
        return f"Customer: {self.customer_name}, Book: {self.book_name}, Loan Date: {self.loan_date}, Return Date: {self.return_date}"


with app.app_context():
    db.create_all()