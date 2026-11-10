from project import db, app
from sqlalchemy.orm import validates
import re

BOOK_NAME_REGEX = re.compile(r"^[\w\s.,'\-:!?()]{1,64}$")
AUTHOR_REGEX = re.compile(r"^[^\W\d_](?:[^\W\d_]|\s|[.,'\-]){0,63}$")


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
        self.name = name
        self.author = author
        self.year_published = year_published
        self.book_type = book_type
        self.status = status

    @validates('name')
    def validate_name(self, key, value):
        if not isinstance(value, str) or not BOOK_NAME_REGEX.match(value.strip()):
            raise ValueError("Invalid book name")
        return value.strip()

    @validates('author')
    def validate_author(self, key, value):
        if not isinstance(value, str) or not AUTHOR_REGEX.match(value.strip()):
            raise ValueError("Invalid author name")
        return value.strip()

    def __repr__(self):
        return f"Book(ID: {self.id}, Name: {self.name}, Author: {self.author}, Year Published: {self.year_published}, Type: {self.book_type}, Status: {self.status})"


with app.app_context():
    db.create_all()
