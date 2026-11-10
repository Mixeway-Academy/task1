from project import db, app
import re
from sqlalchemy.orm import validates

CHAR_NAME = re.compile(r'^[A-Za-z0-9ĄąĆćĘęŁłŃńÓóŚśŹźŻż \.,\-\!\?\':;]{1,80}$')
CHAR_AUTHOR = re.compile(r'^[A-Za-zĄąĆćĘęŁłŃńÓóŚśŹźŻż \.,\-\!\?\':;]{1,80}$')

# Book model
class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    author = db.Column(db.String(64))
    year_published = db.Column(db.Integer) 
    book_type = db.Column(db.String(20))
    status = db.Column(db.String(20), default='available')

    @validates('name')
    def validate_name(self, key, name):
        if not name or not CHAR_NAME.match(name):
            raise ValueError("Invalid book name.")
        return name

    @validates('author')
    def validate_author(self, key, author):
        if not author or not CHAR_AUTHOR.match(author):
            raise ValueError("Invalid author name.")
        return author

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