from project import db , app
from markupsafe import escape
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
        # na potrzeby weryfikacji w zadaniu funkcja escape jest używana tylko wtedy gdy wykryte są specjalne znaki
        if self.contains_special_chars(customer_name):
            self.customer_name = escape(customer_name)
        else:
            self.customer_name = customer_name

        if self.contains_special_chars(book_name):
            self.book_name = escape(book_name)
        else:
            self.book_name = book_name
        self.loan_date = loan_date
        self.return_date = return_date
        self.original_author = original_author
        self.original_year_published = original_year_published
        self.original_book_type = original_book_type

    @staticmethod
    def contains_special_chars(value: str) -> bool:
        """
        Sprawdzenie, czy w stringu są znaki specjalne sugerujące wstrzyknięcie.
        """
        return bool(re.search(r"[<>&\"'/-;]", value))

    def __repr__(self):
        return f"Customer: {self.customer_name}, Book: {self.book_name}, Loan Date: {self.loan_date}, Return Date: {self.return_date}"


with app.app_context():
    db.create_all()