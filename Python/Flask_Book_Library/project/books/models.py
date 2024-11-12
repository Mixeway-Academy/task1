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

    def __init__(self, name, author, year_published, book_type, status='available'):
        if len(name) < 1 or len(name) > 255:
            raise ValueError('Name must have between 1-255 characters')
        if len(author) < 1 or len(author) > 255:
            raise ValueError('Author must have between 1-255 characters')
        if name is None or not re.match("^[\w\d .\'\"()&!@#$%*;:_-]+$", name):
            raise ValueError('Name contains invalid characters or is empty')
        if author is None or not re.match("^[\w\d .\'\"()&!@#$%*;:_-]+$", author):
            raise ValueError('Author name contains invalid characters or is empty')
        self.name = name
        self.author = author
        self.year_published = year_published
        self.book_type = book_type
        self.status = status

    def __repr__(self):
        return f"Book(ID: {self.id}, Name: {self.name}, Author: {self.author}, Year Published: {self.year_published}, Type: {self.book_type}, Status: {self.status})"


with app.app_context():
    db.create_all()