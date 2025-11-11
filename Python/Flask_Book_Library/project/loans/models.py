# models.py
from project import db, app
import html
import re
import unicodedata


def sanitize_input(value: str, max_length: int = 64) -> str:
    if not isinstance(value, str):
        raise ValueError("Wartość musi być tekstem")

    # Normalizacja, przycięcie spacji
    value = unicodedata.normalize('NFC', value.strip())

    # Odrzucenie znaków sterujących i potencjalnych tagów HTML
    if re.search(r'<|>|javascript:|on\w+=', value, re.IGNORECASE):
        # Escape całej wartości — nic nie przepuszczamy
        value = html.escape(value)

    # Ograniczenie długości
    if len(value) > max_length:
        value = value[:max_length]

    return value


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

    def __init__(self, customer_name, book_name, loan_date, return_date,
                 original_author, original_year_published, original_book_type):

        # Sanitizacja wszystkich pól tekstowych
        self.customer_name = sanitize_input(customer_name)
        self.book_name = sanitize_input(book_name)
        self.loan_date = loan_date
        self.return_date = return_date
        self.original_author = sanitize_input(original_author)
        self.original_year_published = original_year_published
        self.original_book_type = sanitize_input(original_book_type)

    def __repr__(self):
        return (f"Customer: {self.customer_name}, Book: {self.book_name}, "
                f"Loan Date: {self.loan_date}, Return Date: {self.return_date}")


with app.app_context():
    db.create_all()
