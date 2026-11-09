from sqlalchemy.orm import validates

from project import db, app
from project.validators import (
    validate_author,
    validate_book_title,
    validate_book_type,
    validate_year_published,
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
        self.name = name
        self.author = author
        self.year_published = year_published
        self.book_type = book_type
        self.status = status

    # Input validation on every assignment (constructor and edits).
    @validates('name')
    def _check_name(self, key, value):
        return validate_book_title(value, key)

    @validates('author')
    def _check_author(self, key, value):
        return validate_author(value, key)

    @validates('year_published')
    def _check_year_published(self, key, value):
        return validate_year_published(value, key)

    @validates('book_type')
    def _check_book_type(self, key, value):
        return validate_book_type(value, key)

    def __repr__(self):
        return f"Book(ID: {self.id}, Name: {self.name}, Author: {self.author}, Year Published: {self.year_published}, Type: {self.book_type}, Status: {self.status})"


with app.app_context():
    db.create_all()