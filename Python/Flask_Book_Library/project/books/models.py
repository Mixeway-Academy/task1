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
        # Zdefiniowane zostają bezpieczne znaki: litery, cyfry, spacje, kropki, przecinki, myślniki.
        # Całkowicie odrzucone zostały nawiasy trójkątne < i >, które służą do ataków XSS.
        safe_pattern = re.compile(r'^[\w\s.,-]*$')

        if not safe_pattern.match(name):
            raise ValueError("Wykryto niedozwolone znaki w tytule książki.")

        if not safe_pattern.match(author):
            raise ValueError("Wykryto niedozwolone znaki w nazwie autora.")

        self.name = name
        self.author = author
        self.year_published = year_published
        self.book_type = book_type
        self.status = status

    def __repr__(self):
        return f"Book(ID: {self.id}, Name: {self.name}, Author: {self.author}, Year Published: {self.year_published}, Type: {self.book_type}, Status: {self.status})"


with app.app_context():
    db.create_all()