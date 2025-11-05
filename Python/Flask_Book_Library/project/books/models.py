from project import db, app
import re
import html


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
        self.name = self._sanitize_input(name)
        self.author = self._sanitize_input(author)
        self.year_published = year_published
        self.book_type = book_type
        self.status = status
    
    def _sanitize_input(self, value):
        """Remove HTML/JS tags and escape dangerous characters"""
        if not value:
            return value
        # Remove script tags and escape HTML
        value = re.sub(r'<script[^>]*>.*?</script>', '', str(value), flags=re.IGNORECASE | re.DOTALL)
        value = html.escape(value)
        return value

    def __repr__(self):
        return f"Book(ID: {self.id}, Name: {self.name}, Author: {self.author}, Year Published: {self.year_published}, Type: {self.book_type}, Status: {self.status})"


with app.app_context():
    db.create_all()