from project import db, app
import re
from sqlalchemy.orm import validates
from datetime import date

# Book model
class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    author = db.Column(db.String(64))
    year_published = db.Column(db.Integer)
    book_type = db.Column(db.String(20))
    status = db.Column(db.String(20), default='available')

    allowed_book_types = ("2days", "5days", "10days")

    @validates('name')
    def validates_name(self, key, value):
        if not isinstance(value, str) or not re.fullmatch(r"[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż0-9 .,:;!?()'„”–-]{1,64}", value):
            raise ValueError("Niepoprawne znaki w polu name")
        return value

    @validates('author')
    def validates_author(self, key, value):
        if not isinstance(value, str) or not re.fullmatch(r"[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż .'-]{1,64}", value):
            raise ValueError("Niepoprawne znaki w polu author")
        return value

    @validates('year_published')
    def validates_year_published(self, key, value):
        if isinstance(value, str) and re.fullmatch(r"-?[0-9]+", value):
            value = int(value)
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError("Niepoprawny rok opublikowania książki")
        if not -10000 <= value <= date.today().year:
            raise ValueError("Niepoprawny rok opublikowania książki")
        return value

    @validates('book_type')
    def validates_book_type(self, key, value):
        if not isinstance(value, str) or value not in self.allowed_book_types:
            raise ValueError("Niepoprawny termin możliwości wypożyczenia książki")
        return value

    @validates('status')
    def validates_status(self, key, value):
        if not isinstance(value, str) or value != 'available':
            raise ValueError("Niepoprawny status książki")
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
