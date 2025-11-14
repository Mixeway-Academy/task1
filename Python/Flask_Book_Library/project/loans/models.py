from datetime import date, datetime
from project import db , app
import re
from project.constants import (
    AUTHOR_NAME_RE, 
    BOOK_NAME_RE, 
    MAX_NAME_OR_AUTHOR_LENGTH, 
    MAX_BOOK_TYPE_OR_STATUS_LENGTH
)

# Loan model
class Loan(db.Model):
    __tablename__ = 'Loans'

    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(MAX_NAME_OR_AUTHOR_LENGTH), nullable=False)
    book_name = db.Column(db.String(MAX_NAME_OR_AUTHOR_LENGTH), nullable=False)
    loan_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime, nullable=False)
    original_author = db.Column(db.String(MAX_NAME_OR_AUTHOR_LENGTH), nullable=False)
    original_year_published = db.Column(db.Integer, nullable=False)
    original_book_type = db.Column(db.String(MAX_BOOK_TYPE_OR_STATUS_LENGTH), nullable=False)

    def __init__(self, customer_name, book_name, loan_date, return_date, original_author, original_year_published, original_book_type):
        customer_name = customer_name.strip()
        book_name = book_name.strip()
        original_author = original_author.strip()
        original_book_type = original_book_type.strip()
        
        if len(customer_name) > MAX_NAME_OR_AUTHOR_LENGTH or not AUTHOR_NAME_RE.fullmatch(customer_name):
            raise ValueError("Invalid customer name format or length.")
        
        if len(book_name) > MAX_NAME_OR_AUTHOR_LENGTH or not BOOK_NAME_RE.fullmatch(book_name):
            raise ValueError("Invalid book name format or length.")
            
        if len(original_author) > MAX_NAME_OR_AUTHOR_LENGTH or not AUTHOR_NAME_RE.fullmatch(original_author):
            raise ValueError("Invalid original author name format or length.")
        
        if len(original_book_type) > MAX_BOOK_TYPE_OR_STATUS_LENGTH:
             raise ValueError("Original book type too long.")

    
        current_year = date.today().year
        if not isinstance(original_year_published, int) or original_year_published > current_year or original_year_published < 0:
            raise ValueError("Original year published must be between 0 and the current year.")
        
        if not isinstance(loan_date, (date, datetime)):
            raise ValueError("Loan date must be a valid date object.")
        if not isinstance(return_date, (date, datetime)):
            raise ValueError("Return date must be a valid date object.")
        
        loan_date_obj = loan_date.date() if isinstance(loan_date, datetime) else loan_date
        return_date_obj = return_date.date() if isinstance(return_date, datetime) else return_date

        if return_date_obj < loan_date_obj:
            raise ValueError("Return date cannot be before the loan date.")
        
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