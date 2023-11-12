from project import db, app
import re
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

    def __repr__(self):
        return f"Book(ID: {self.id}, Name: {self.name}, Author: {self.author}, Year Published: {self.year_published}, Type: {self.book_type}, Status: {self.status})"

    @validates('name')
    def validate_name(self, key, value):
        regex = r"^[A-Za-z0-9\s]*$"

        if not re.match(regex, value):
            raise ValueError("The only allowed characters in \"Name\" field are: alphanumeric characters, spaces")
        return value

    @validates('author')
    def validate_author(self, key, value):
        regex = r"^[A-Za-z\s]*$"

        if not re.match(regex, value):
            raise ValueError("The only allowed characters in \"Author\" field are: alphabetic characters, spaces")
        return value


with app.app_context():
    db.create_all()
