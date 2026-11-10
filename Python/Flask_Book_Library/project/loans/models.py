from project import db, app
import re
from datetime import datetime


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

    def __init__(
        self,
        customer_name,
        book_name,
        loan_date,
        return_date,
        original_author,
        original_year_published,
        original_book_type
    ):
        self.customer_name = self.validate_text(
            customer_name, "Nazwa klienta", 64
        )

        self.book_name = self.validate_text(
            book_name, "Nazwa książki", 64
        )

        self.original_author = self.validate_text(
            original_author, "Autor", 64
        )

        self.original_book_type = self.validate_text(
            original_book_type, "Typ książki", 64
        )

        self.original_year_published = self.validate_year(
            original_year_published
        )

        self.loan_date = self.validate_date(loan_date, "Data wypożyczenia")
        self.return_date = self.validate_date(return_date, "Data zwrotu")

        if self.return_date <= self.loan_date:
            raise ValueError(
                "Data zwrotu musi być późniejsza niż data wypożyczenia"
            )

    @staticmethod
    def validate_text(value, field_name, max_length):
        """
        Walidacja pól tekstowych i zabezpieczenie przed HTML/XSS.
        """

        if not isinstance(value, str):
            raise ValueError(f"{field_name} musi być tekstem")

        value = value.strip()

        if not value:
            raise ValueError(f"{field_name} nie może być puste")

        if len(value) > max_length:
            raise ValueError(
                f"{field_name} może mieć maksymalnie {max_length} znaków"
            )

        # Odrzucanie znaczników HTML
        if re.search(r"<[^>]*>", value):
            raise ValueError(
                f"{field_name} nie może zawierać znaczników HTML"
            )

        return value

    @staticmethod
    def validate_year(value):
        """
        Walidacja roku wydania książki.
        """

        if isinstance(value, bool):
            raise ValueError("Rok wydania musi być liczbą całkowitą")

        try:
            year = int(value)
        except (ValueError, TypeError):
            raise ValueError("Rok wydania musi być liczbą całkowitą")

        if year < 1 or year > 2026:
            raise ValueError("Niepoprawny rok wydania")

        return year

    @staticmethod
    def validate_date(value, field_name):
        """
        Walidacja daty wypożyczenia i zwrotu.
        """

        if isinstance(value, str):
            try:
                value = datetime.fromisoformat(value)
            except ValueError:
                raise ValueError(
                    f"{field_name} ma niepoprawny format"
                )

        if not isinstance(value, datetime):
            raise ValueError(
                f"{field_name} musi być poprawną datą"
            )

        return value

    def __repr__(self):
        return (
            f"Customer: {self.customer_name}, "
            f"Book: {self.book_name}, "
            f"Loan Date: {self.loan_date}, "
            f"Return Date: {self.return_date}"
        )


with app.app_context():
    db.create_all()
