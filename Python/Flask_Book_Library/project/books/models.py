from project import db, app
import re
import bleach

XSS_REGEX = re.compile(r'^(?!.*<)(?!.*>)(?!.*["\'])(?!.*/)(?!.*=)[\w\sÀ-ÖØ-öø-ÿ\-\.,\'()]+$')
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
        self.name = bleach.clean(name, tags=[], strip=True)
        self.author = bleach.clean(author, tags=[], strip=True)
        self.year_published = bleach.clean(year_published, tags=[], strip=True)
        self.book_type = bleach.clean(book_type, tags=[], strip=True)
        self.status = bleach.clean(status, tags=[], strip=True)

    def __repr__(self):
        return f"Book(ID: {self.id}, Name: {self.name}, Author: {self.author}, Year Published: {self.year_published}, Type: {self.book_type}, Status: {self.status})"


with app.app_context():
    db.create_all()