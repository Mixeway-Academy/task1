from project import db , app
from sqlalchemy.orm import validates
import re


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

    VALID_NAME_PATTERN = r'^[a-zA-Z\s\.-]*$'
    VALID_BOOK_NAME_PATTERN = r'^[a-zA-Z0-9\s,\.-?!:]*$'
    max_len = 64

    @validates('book_name', 'customer_name', 'original_author')
    def validate_name_and_book_name(self, key, value):
        if len(value) > self.max_len:
            raise ValueError(f"{key.capitalize()} too long.")
        pattern = self.VALID_BOOK_NAME_PATTERN if key == 'book_name' else self.VALID_NAME_PATTERN
        if not re.match(pattern, value):
            raise ValueError(f"{key.capitalize()} contains invalid characters.")
        return value

    def __init__(self, customer_name, book_name, loan_date, return_date, original_author, original_year_published, original_book_type):
        self.customer_name = customer_name
        self.book_name = book_name
        self.loan_date = loan_date
        self.return_date = return_date
        self.original_author = original_author
        self.original_year_published = original_year_published
        self.original_book_type = original_book_type

    def __repr__(self):
        return f"Customer: {self.customer_name}, Book: {self.book_name}, Loan Date: {self.loan_date}, Return Date: {self.return_date}"


with app.app_context():
    db.create_all()