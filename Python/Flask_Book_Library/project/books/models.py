from project import db, app
import re


# Book model
class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True, nullable=False)
    author = db.Column(db.String(64), nullable=False)
    year_published = db.Column(db.Integer, nullable=False)
    book_type = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default='available', nullable=False)

    def __init__(self, name, author, year_published, book_type, status='available'):

        self.name = self.validate_text(name, "Nazwa książki", 64)
        self.author = self.validate_text(author, "Autor", 64)
        self.book_type = self.validate_text(book_type, "Typ książki", 20)
        self.status = self.validate_text(status, "Status", 20)

        self.year_published = self.validate_year(year_published)

    @staticmethod
    def validate_text(value, field_name, max_length):
        """
        Walidacja pól tekstowych.
        Odrzuca puste wartości, zbyt długie teksty
        oraz znaczniki HTML.
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

        # Blokowanie znaczników HTML, które mogą prowadzić do XSS
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

    def __repr__(self):
        return (
            f"Book(ID: {self.id}, Name: {self.name}, "
            f"Author: {self.author}, Year Published: {self.year_published}, "
            f"Type: {self.book_type}, Status: {self.status})"
        )


with app.app_context():
    db.create_all()
