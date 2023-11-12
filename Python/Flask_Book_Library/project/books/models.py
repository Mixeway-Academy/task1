import re

from project import db, app


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
        self._validate_name(name)
        self._validate_author(author)

        self.name = name
        self.author = author
        self.year_published = year_published
        self.book_type = book_type
        self.status = status

    def _update_name(self, new_name):
        self._validate_name(new_name)
        self.name = new_name

    def _update_author(self, new_author):
        self._validate_author(new_author)
        self.author = new_author

    def _validate_name(self, name):
        if not re.fullmatch(r'[a-zA-Z0-9 ,:.!?]{1,64}', name):
            raise ValueError('Name must not be longer than 64 characters or contain special characters other than:    ,:.!?')

    def _validate_author(self, author):
        if not re.fullmatch(r'[a-zA-Z ]{1,64}', author):
            raise ValueError('Author must not be longer than 64 characters or contain numbers or special characters')

    def __repr__(self):
        return f"Book(ID: {self.id}, Name: {self.name}, Author: {self.author}, Year Published: {self.year_published}, Type: {self.book_type}, Status: {self.status})"


with app.app_context():
    db.create_all()