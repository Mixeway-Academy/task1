from project import db, app
import re


# Whitelist: letters, digits, spaces and basic punctuation only (blocks HTML/JS)
BOOK_TEXT_RE = re.compile(r'^[A-Za-z0-9ĄąĆćĘęŁłŃńÓóŚśŹźŻż .,\-]{1,64}$')


def validate_book_text(value, field_name):
    if not isinstance(value, str) or not BOOK_TEXT_RE.match(value):
        raise ValueError(
            f'Invalid {field_name}: only letters, digits, spaces and .,- are allowed (max 64 chars)'
        )


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
        validate_book_text(name, 'name')
        validate_book_text(author, 'author')
        self.name = name
        self.author = author
        self.year_published = year_published
        self.book_type = book_type
        self.status = status

    def __repr__(self):
        return f"Book(ID: {self.id}, Name: {self.name}, Author: {self.author}, Year Published: {self.year_published}, Type: {self.book_type}, Status: {self.status})"


with app.app_context():
    db.create_all()
