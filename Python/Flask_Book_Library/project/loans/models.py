from project import db , app
import bleach

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
        self.customer_name = bleach.clean(customer_name, tags=[], strip=True)
        self.book_name = bleach.clean(book_name, tags=[], strip=True)
        self.loan_date = bleach.clean(loan_date, tags=[], strip=True)
        self.return_date = bleach.clean(return_date, tags=[], strip=True)
        self.original_author = bleach.clean(original_author, tags=[], strip=True)
        self.original_year_published = bleach.clean(original_year_published, tags=[], strip=True)
        self.original_book_type = bleach.clean(original_book_type, tags=[], strip=True)

    def __repr__(self):
        return f"Customer: {self.customer_name}, Book: {self.book_name}, Loan Date: {self.loan_date}, Return Date: {self.return_date}"


with app.app_context():
    db.create_all()