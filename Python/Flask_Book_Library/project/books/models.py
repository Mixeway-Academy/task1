from sqlalchemy.orm import validates

from project import db, app
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

    max_len = 64
    pattern = '^[a-zA-Z0-9\s-]*$'

    @validates('name', 'author')
    def validate(self, key, value):
        if len(value) > self.max_len:
            raise ValueError(f"{key.capitalize()} is too long!")
        if not re.match(self.pattern, value):
            raise ValueError(f"{key.capitalize()} has invalid characters.")
        return value

    def __init__(self, name, author, year_published, book_type, status='available'):
        self.name = name
        self.author = author
        self.year_published = year_published
        self.book_type = book_type
        self.status = status

    def __repr__(self):
        return f"Book(ID: {self.id}, Name: {self.name}, Author: {self.author}, Year Published: {self.year_published}, Type: {self.book_type}, Status: {self.status})"


with app.app_context():
    db.create_all()
