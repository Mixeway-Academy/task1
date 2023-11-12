from project import db, app
import re
from sqlalchemy.orm import validates


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

    customer_name_pattern = re.compile('^[a-z \'"-]{1,64}$', re.IGNORECASE)
    book_name_pattern = re.compile('^[a-z0-9 ()!\'"/$=*&:,.?-]{1,64}$', re.IGNORECASE)
    original_author_pattern = re.compile('^[a-z \'"-]{1,64}$', re.IGNORECASE)

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
    def validate_customer_name(self, _, customer_name):
        customer_name = str(customer_name)
        (min_len, max_len) = (1, 64)
        if not min_len <= len(customer_name) <= max_len:
            raise ValueError(f'Expected customer_name to have length between {min_len} and {max_len}, but it has length equal to {len(customer_name)} instead')
        if re.fullmatch(self.customer_name_pattern, customer_name) is None:
            raise ValueError(f'Provided customer_name value does not match pattern {self.customer_name_pattern}')
        return customer_name

    @validates('book_name')
    def validate_book_name(self, _, book_name):
        book_name = str(book_name)
        (min_len, max_len) = (1, 64)
        if not min_len <= len(book_name) <= max_len:
            raise ValueError(f'Expected book_name to have length between {min_len} and {max_len}, but it has length equal to {len(book_name)} instead')
        if re.fullmatch(self.book_name_pattern, book_name) is None:
            raise ValueError(f'Provided book_name value does not match pattern {self.book_name_pattern}')
        return book_name

    @validates('original_author')
    def validate_original_author(self, _, original_author):
        original_author = str(original_author)
        (min_len, max_len) = (1, 64)
        if not min_len <= len(original_author) <= max_len:
            raise ValueError(f'Expected original_author to have length between {min_len} and {max_len}, but it has length equal to {len(original_author)} instead')
        if re.fullmatch(self.original_author_pattern, original_author) is None:
            raise ValueError(f'Provided original_author value does not match pattern {self.original_author_pattern}')
        return original_author

    @validates('original_year_published')
    def validate_original_year_published(self, _, original_year_published):
        original_year_published = int(original_year_published)
        (min_value, max_value) = (500, 2500)
        if not min_value <= original_year_published <= max_value:
            raise ValueError(f'Expected original_year_published to be between {min_value} and {max_value}, but it is {original_year_published} instead')
        return original_year_published

    @validates('original_book_type')
    def validate_original_book_type(self, _, original_book_type):
        original_book_type = str(original_book_type)
        allowed_values = ['2days', '5days', '10days']
        if original_book_type not in allowed_values:
            raise ValueError(f'Invalid book type value {original_book_type}, expected one of [{", ".join(allowed_values)}]')
        return original_book_type


with app.app_context():
    db.create_all()