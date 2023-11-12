from project import db, app
import re

# Model Książki
class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    author = db.Column(db.String(64))
    year_published = db.Column(db.Integer) 
    book_type = db.Column(db.String(20))
    status = db.Column(db.String(20), default='available')

    def __init__(self, name, author, year_published, book_type, status='available'):
        # Walidacja nazwy książki
        if not 1 <= len(name) <= 64:
            raise ValueError("Nazwa książki musi mieć od 1 do 64 znaków.")
        
        if any(char in "!@#$%^&*()_+=[]{};:'\"<>,./?\\|" for char in name):
            raise ValueError("Nazwa książki zawiera niedozwolone znaki.")

        # Walidacja nazwiska autora
        if not 1 <= len(author) <= 64:
            raise ValueError("Nazwisko autora musi mieć od 1 do 64 znaków.")
        
        if any(char in "!@#$%^&*()_+=[]{};:'\"<>,./?\\|" for char in author):
            raise ValueError("Nazwisko autora zawiera niedozwolone znaki.")

        self.name = name
        self.author = author
        self.year_published = year_published
        self.book_type = book_type
        self.status = status

    def __repr__(self):
        return f"Book(ID: {self.id}, Name: {self.name}, Author: {self.author}, Year Published: {self.year_published}, Type: {self.book_type}, Status: {self.status})"

with app.app_context():
    db.create_all()
