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
        self.name = name
        self.author = author
        self.year_published = year_published
        self.book_type = book_type
        self.status = status

    def __repr__(self):
        return f"Book(ID: {self.id}, Name: {self.name}, Author: {self.author}, Year Published: {self.year_published}, Type: {self.book_type}, Status: {self.status})"

    def is_valid(self):
        if len(self.name) > 64:
            return False
        if len(self.author) > 64:
            return False
        if not self.year_published.isnumeric():
            return False
        if len(self.book_type) > 20 or not (self.book_type == '2days' or self.book_type == '5days' or self.book_type == '10days'):
            return False
        return True

with app.app_context():
    db.create_all()