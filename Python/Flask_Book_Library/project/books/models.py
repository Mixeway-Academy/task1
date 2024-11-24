from project import db, app
from sqlalchemy.orm import validates
import re


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

    def __repr__(self):
        return f"Book(ID: {self.id}, Name: {self.name}, Author: {self.author}, Year Published: {self.year_published}, Type: {self.book_type}, Status: {self.status})"

    @validates('name')
    def name_validator(self, key, value):
        if not value:
            raise ValueError("Name must not be blank")
        if re.match(r'^[a-zA-Z0-9 ]+$', value) is None:
            raise ValueError("Name must contain only letters, numbers, and spaces")
        return value

    @validates("author")
    def author_validator(self, key, value):
        if not value:
            raise ValueError("Author must not be blank")
        if re.match(r'^[a-zA-Z ]+$', value) is None:
            raise ValueError("Author must contain only letters and spaces")
        return value

with app.app_context():
    db.create_all()