from project import db, app
import re
from sqlalchemy.orm import validates

# Zgodnie z koncepcją ograniczania typów prostych i hermetyzacji (Primitive Obsession)
CHAR_NAME = re.compile(r'^[A-Za-z0-9ĄąĆćĘęŁłŃńÓóŚśŹźŻż \.,\-\!\?\':;]{1,80}$')
CHAR_AUTHOR = re.compile(r'^[A-Za-zĄąĆćĘęŁłŃńÓóŚśŹźŻż \.\-]{1,80}$')

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

    @validates('customer_name')
    def validate_customer_name(self, key, customer_name):
        if not customer_name or not CHAR_NAME.match(customer_name):
            raise ValueError("Invalid customer name.")
        return customer_name

    @validates('book_name')
    def validate_book_name(self, key, book_name):
        if not book_name or not CHAR_NAME.match(book_name):
            raise ValueError("Invalid book name.")
        return book_name

    @validates('original_author')
    def validate_original_author(self, key, original_author):
        if not original_author or not CHAR_AUTHOR.match(original_author):
            raise ValueError("Invalid author name.")
        return original_author

    @validates('original_book_type')
    def validate_original_book_type(self, key, original_book_type):
        if not original_book_type or not CHAR_NAME.match(original_book_type):
            raise ValueError("Invalid book type.")
        return original_book_type

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