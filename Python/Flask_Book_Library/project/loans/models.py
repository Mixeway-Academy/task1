from project import db , app
from project.validators.text_validator import validate_text


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
        self.customer_name = validate_text(customer_name)
        self.book_name = validate_text(book_name)
        self.loan_date = loan_date
        self.return_date = return_date
        self.original_author = validate_text(original_author)
        self.original_year_published = original_year_published
        self.original_book_type = validate_text(original_book_type)

    def validate(self):
        self.customer_name = validate_text(self.customer_name)
        self.book_name = validate_text(self.book_name)
        self.original_author = validate_text(self.original_author)
        self.original_book_type = validate_text(self.original_book_type)

    def __repr__(self):
        return f"Customer: {self.customer_name}, Book: {self.book_name}, Loan Date: {self.loan_date}, Return Date: {self.return_date}"


with app.app_context():
    db.create_all()