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

    # Walidacja pola tekstowego za pomocą wyrażenia regularnego
    def validate_text(self, text):
        if not re.match("^[a-zA-Z0-9\s-]*$", text):
            raise ValueError("Dozwolone są tylko małe i wielkie litery, cyfry, spacja oraz myślnik.")
        return text

    def __init__(self, name, author, year_published, book_type, status='available'):
        # Walidacja każdego z pól tekstowych
        self.name = self.validate_text(name)
        self.author = self.validate_text(author)
        self.book_type = self.validate_text(book_type)
        self.status = self.validate_text(status)
        self.year_published = year_published

    def __repr__(self):
        return f"Book(ID: {self.id}, Name: {self.name}, Author: {self.author}, Year Published: {self.year_published}, Type: {self.book_type}, Status: {self.status})"


with app.app_context():
    db.create_all()
