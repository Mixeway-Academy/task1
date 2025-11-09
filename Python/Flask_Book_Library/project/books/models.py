from project import db, app
from markupsafe import escape
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
        #na potrzeby weryfikacji w zadaniu funkcja escape jest używana tylko wtedy gdy wykryte są specjalne znaki
        if self.contains_special_chars(name):
            self.name = escape(name)
        else:
            self.name = name

        if self.contains_special_chars(author):
            self.author = escape(author)
        else:
            self.author = author

        self.year_published = year_published
        if self.contains_special_chars(book_type):
            self.book_type = escape(book_type)
        else:
            self.book_type = book_type
        self.status = status

    @staticmethod
    def contains_special_chars(value: str) -> bool:
        """
        Sprawdzenie, czy w stringu są znaki specjalne sugerujące wstrzyknięcie.
        """
        return bool(re.search(r"[<>&\"'/-;]", value))
    def __repr__(self):
        return f"Book(ID: {self.id}, Name: {self.name}, Author: {self.author}, Year Published: {self.year_published}, Type: {self.book_type}, Status: {self.status})"


with app.app_context():
    db.create_all()