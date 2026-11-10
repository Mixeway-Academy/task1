from sqlalchemy.orm import validates

from project import app, db
from project.validators import validate_choice, validate_number, validate_text

BOOK_TYPES = ('2days', '5days', '10days')


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

    # Validators run on every assignment (in __init__ and when editing),
    # so invalid data never reaches the database.
    @validates('name', 'author')
    def _validate_text(self, key, value):
        return validate_text(value, key)

    @validates('year_published')
    def _validate_number(self, key, value):
        return validate_number(value, key)

    @validates('book_type')
    def _validate_book_type(self, key, value):
        return validate_choice(value, key, BOOK_TYPES)

    def __repr__(self):
        return f"Book(ID: {self.id}, Name: {self.name}, Author: {self.author}, Year Published: {self.year_published}, Type: {self.book_type}, Status: {self.status})"


with app.app_context():
    db.create_all()