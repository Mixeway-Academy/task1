from project import db, app
import html
import re
import unicodedata


def sanitize_input(value: str, max_length: int = 64) -> str:
    if not isinstance(value, str):
        raise ValueError("Wartość musi być tekstem")

    value = unicodedata.normalize('NFC', value.strip())

    # Odrzuć znaczniki HTML i JS
    if re.search(r'<|>|javascript:|on\w+=', value, re.IGNORECASE):
        value = html.escape(value)

    if len(value) > max_length:
        value = value[:max_length]

    return value


# Book model
class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    author = db.Column(db.String(64))
    year_published = db.Column(db.Integer)
    book_type = db.Column(db.String(20))
    status = db.Column(db.String(20), default='available')

    def __init__(self, name, author, year_published, book_type, status='available'):
        # Walidacja i sanitizacja
        self.name = sanitize_input(name)
        self.author = sanitize_input(author)
        self.year_published = year_published
        self.book_type = sanitize_input(book_type, 20)
        self.status = sanitize_input(status, 20)

    def __repr__(self):
        return (f"Book(ID: {self.id}, Name: {self.name}, Author: {self.author}, "
                f"Year Published: {self.year_published}, Type: {self.book_type}, Status: {self.status})")


with app.app_context():
    db.create_all()
