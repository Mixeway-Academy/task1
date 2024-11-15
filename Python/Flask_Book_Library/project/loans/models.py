import re

from project import db, app

from project.books.models import BookChecker
from project.customers.models import CustomerChecker

class LoanChecker(BookChecker, CustomerChecker):

    def check_date(self, date):  # TODO
        # REQUEST YYYY-MM-DD
        if not isinstance(date, str) or not re.match(r'^\d{4}-\d{2}-\d{2}$', date):
            raise ValueError("Date must be in the format YYYY-MM-DD")
        return True

    def check_loan(self, loan):
        print(f'{loan.customer_name=} {loan.book_name=} {loan.loan_date=} {loan.return_date=}')
        if (
            self.check_name(loan.customer_name)
            and self.check_name(loan.book_name)
            and self.check_date(loan.loan_date)
            and self.check_date(loan.return_date)
        ):
            return True
        raise ValueError("Loan data is invalid")

checker = LoanChecker()

# Loan model
class Loan(db.Model):
    __tablename__ = "Loans"

    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(64), nullable=False)
    book_name = db.Column(db.String(64), nullable=False)
    loan_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime, nullable=False)
    original_author = db.Column(db.String(64), nullable=False)
    original_year_published = db.Column(db.Integer, nullable=False)
    original_book_type = db.Column(db.String(64), nullable=False)

    def __init__(
        self,
        customer_name,
        book_name,
        loan_date,
        return_date,
        original_author,
        original_year_published,
        original_book_type,
    ):
        
        self.customer_name =  customer_name if checker.check_name(customer_name) else None
        self.book_name = book_name if checker.check_name(book_name) else None
        self.loan_date = loan_date if checker.check_date(loan_date) else None
        self.return_date = return_date if checker.check_date(return_date) else None
        self.original_author = original_author
        self.original_year_published = original_year_published
        self.original_book_type = original_book_type

    def __repr__(self):
        return f"Customer: {self.customer_name}, Book: {self.book_name}, Loan Date: {self.loan_date}, Return Date: {self.return_date}"


with app.app_context():
    db.create_all()
