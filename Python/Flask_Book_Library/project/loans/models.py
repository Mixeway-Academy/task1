from project import db, app
import re


# Whitelist: letters, digits, spaces and basic punctuation only (blocks HTML/JS)
LOAN_TEXT_RE = re.compile(r'^[A-Za-z0-9ĄąĆćĘęŁłŃńÓóŚśŹźŻż .,\-]{1,64}$')


def validate_loan_text(value, field_name):
    if not isinstance(value, str) or not LOAN_TEXT_RE.match(value):
        raise ValueError(
            f'Invalid {field_name}: only letters, digits, spaces and .,- are allowed (max 64 chars)'
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
        validate_loan_text(customer_name, 'customer_name')
        validate_loan_text(book_name, 'book_name')
        validate_loan_text(original_author, 'original_author')
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
