from project import db, app
import re

BOOK_NAME_ALLOWED_PATTERN = re.compile(r"^[A-Za-z0-9À-ž\s\.\,\-']+$")
AUTHOR_ALLOWED_PATTERN = re.compile(r"^[A-Za-z0-9À-ž\s\.\,\-']+$")

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
        if BOOK_NAME_ALLOWED_PATTERN.match(name):
            self.name = name
        if AUTHOR_ALLOWED_PATTERN.match(author):
            self.author = author
        self.year_published = year_published
        self.book_type = book_type
        self.status = status

    def __repr__(self):
        return f"Book(ID: {self.id}, Name: {self.name}, Author: {self.author}, Year Published: {self.year_published}, Type: {self.book_type}, Status: {self.status})"


with app.app_context():
    db.create_all()