from project import db, app
from markupsafe import escape
from sqlalchemy.ext.hybrid import hybrid_property

# Book model
class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column("name", db.String(64), unique=True, index=True)
    _author = db.Column("author", db.String(64))
    year_published = db.Column(db.Integer)
    book_type = db.Column(db.String(20))
    status = db.Column(db.String(20), default='available')

    def __init__(self, name, author, year_published, book_type, status='available'):
        self.name = name
        self.author = author
        self.year_published = year_published
        self.book_type = book_type
        self.status = status

    @hybrid_property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = escape(value)

    @name.expression
    def name(cls):
        return cls._name

    @hybrid_property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        self._author = escape(value)

    @author.expression
    def author(cls):
        return cls._author

    def __repr__(self):
        return f"Book(ID: {self.id}, Name: {self.name}, Author: {self.author}, Year Published: {self.year_published}, Type: {self.book_type}, Status: {self.status})"


with app.app_context():
    db.create_all()