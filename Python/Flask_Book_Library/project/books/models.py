from project import db, app
import re
from sqlalchemy.orm import validates


TEXT_PATTERN = re.compile(r"^[\w\s.,:;!?'\"()\-]+$", re.UNICODE)
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

    # Walidacja danych wejściowych
    @validates('name', 'author')
    def validate_text(self, key, value):
        if isinstance(value, str):
            value = re.sub(r"\s+", " ", value.strip())
        if not isinstance(value, str) or not 1 <= len(value) <= 64 or not TEXT_PATTERN.match(value):
            raise ValueError(f"Pole '{key}' zawiera niedozwolone znaki")
        return value


    def __repr__(self):
        return f"Book(ID: {self.id}, Name: {self.name}, Author: {self.author}, Year Published: {self.year_published}, Type: {self.book_type}, Status: {self.status})"


with app.app_context():
    db.create_all()