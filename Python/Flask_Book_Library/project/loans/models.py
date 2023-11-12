from project import db, app
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

    @validates('customer_name')
    def validate_customer_name(self, _, value):
        regex = r"^[A-Za-z\s]*$"

        if not re.match(regex, value):
            raise ValueError("The only allowed characters in \"Customer Name\" field are: alphabetic characters")
        return value

    @validates('book_name')
    def validate_book_name(self, _, value):
        regex = r"^[A-Za-z0-9\s]*$"

        if not re.match(regex, value):
            raise ValueError("The only allowed characters in \"Book Name\" field are: alphanumeric characters, spaces")
        return value

    @validates('original_author')
    def validate_original_author(self, _, value):
        regex = r"^[A-Za-z\s]*$"

        if not re.match(regex, value):
            raise ValueError("The only allowed characters in \"Author\" field are: alphanumeric characters, spaces")
        return value


with app.app_context():
    db.create_all()
