from project import db, app
import re
from datetime import date
from project.constants import BOOK_NAME_RE, AUTHOR_NAME_RE, MAX_NAME_OR_AUTHOR_LENGTH, MAX_BOOK_TYPE_OR_STATUS_LENGTH


# Book model
class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(MAX_NAME_OR_AUTHOR_LENGTH), unique=True, index=True)
    author = db.Column(db.String(MAX_NAME_OR_AUTHOR_LENGTH))
    year_published = db.Column(db.Integer) 
    book_type = db.Column(db.String(MAX_BOOK_TYPE_OR_STATUS_LENGTH))
    status = db.Column(db.String(MAX_BOOK_TYPE_OR_STATUS_LENGTH), default='available')

    def __init__(self, name, author, year_published, book_type, status='available'):

        name = name.strip()
        author = author.strip()
        book_type = book_type.strip()
        status = status.strip()

        if len(name) > MAX_NAME_OR_AUTHOR_LENGTH or not BOOK_NAME_RE.fullmatch(name):
            raise ValueError("Invalid book name format or length.")

        if len(author) > MAX_NAME_OR_AUTHOR_LENGTH or not AUTHOR_NAME_RE.fullmatch(author):
            raise ValueError("Invalid author name format or length.")
        
        current_year = date.today().year
        if year_published > current_year or year_published < 0:
            raise ValueError("Year published must be between 0 and the current year.")

        if len(book_type) > MAX_BOOK_TYPE_OR_STATUS_LENGTH:
            raise ValueError("Book type too long.")
        if len(status) > MAX_BOOK_TYPE_OR_STATUS_LENGTH:
            raise ValueError("Status too long.")

        self.name = name
        self.author = author
        self.year_published = year_published
        self.book_type = book_type
        self.status = status

    def __repr__(self):
        return f"Book(ID: {self.id}, Name: {self.name}, Author: {self.author}, Year Published: {self.year_published}, Type: {self.book_type}, Status: {self.status})"


with app.app_context():
    db.create_all()