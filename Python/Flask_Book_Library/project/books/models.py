from project import db, app
import re
from datetime import datetime
from sqlalchemy.orm import validates

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
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Book name cannot be empty.")
        if len(name) > 64:
            raise ValueError("Book name cannot exceed 64 characters.")
        if not re.match(r'^[a-zA-Z0-9\s\-_]+$', name):
            raise ValueError("Book name contains invalid characters.")
        return name

    @validates('author')
    def validate_author(self, key, author):
        if not author:
            raise ValueError("Author name cannot be empty.")
        if len(author) > 64:
            raise ValueError("Author name cannot exceed 64 characters.")
        if not re.match(r'^[a-zA-Z\s\.\-]+$', author):
            raise ValueError("Author name contains invalid characters.")
        return author

    @validates('year_published')
    def validate_year_published(self, key, year_published):
        try:
            year_published = int(year_published)
        except (ValueError, TypeError):
            raise ValueError("Year published must be a valid integer.")
        if year_published < 0 or year_published > datetime.now().year:
            raise ValueError("Year published must be a valid year.")
        return year_published

    @validates('book_type')
    def validate_book_type(self, key, book_type):
        if book_type not in ['2days', '5days', '10days']:
            raise ValueError("Book type must be either '2days', '5days', or '10days'.")
        return book_type

    @validates('status')
    def validate_status(self, key, status):
        if len(status) > 20:
            raise ValueError("Status name cannot exceed 20 characters.")
        return status

    def __repr__(self):
        return f"Book(ID: {self.id}, Name: {self.name}, Author: {self.author}, Year Published: {self.year_published}, Type: {self.book_type}, Status: {self.status})"


with app.app_context():
    db.create_all()