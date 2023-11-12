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
        if len(name) < 3 and len(name) > 64:
            raise ValueError('Name should have length between 3 and 64 characters!')
        if re.fullmatch(r'[\w\s:\-,]+', name) is None:
            raise ValueError('Inappropriate symbol used: Name should contain only letters, digits, spaces, hyphens, commas and colons!')
        self.name = name
        if len(author) < 3 and len(author) > 64:
            raise ValueError('Author should have length between 3 and 64 characters!')
        if re.fullmatch(r'[\w\s:\-,]+', author) is None:
            raise ValueError('Inappropriate symbol used: Author should contain only letters, digits, spaces, hyphens, commas and colons!')
        self.author = author
        self.year_published = year_published
        self.book_type = book_type
        self.status = status

    def __repr__(self):
        return f"Book(ID: {self.id}, Name: {self.name}, Author: {self.author}, Year Published: {self.year_published}, Type: {self.book_type}, Status: {self.status})"


with app.app_context():
    db.create_all()