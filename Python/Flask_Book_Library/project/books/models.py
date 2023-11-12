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

    name_pattern = re.compile('^[a-z0-9 ()!\'"/$=*&:,.?-]{1,64}$', re.IGNORECASE)
    author_pattern = re.compile('^[a-z \'"-]{1,64}$', re.IGNORECASE)

    def __init__(self, name, author, year_published, book_type, status='available'):
        self.name = name
        self.author = author
        self.year_published = year_published
        self.book_type = book_type
        self.status = status

    def __repr__(self):
        return f"Book(ID: {self.id}, Name: {self.name}, Author: {self.author}, Year Published: {self.year_published}, Type: {self.book_type}, Status: {self.status})"

    @validates('name')
    def validate_name(self, _, name):
        name = str(name)
        (min_len, max_len) = (1, 64)
        if not min_len <= len(name) <= max_len:
            raise ValueError(f'Expected name to have length between {min_len} and {max_len}, but it has length equal to {len(name)} instead')
        if re.fullmatch(self.name_pattern, name) is None:
            raise ValueError(f'Provided name value does not match pattern {self.name_pattern}')
        return name

    @validates('author')
    def validate_author(self, _, author):
        author = str(author)
        (min_len, max_len) = (1, 64)
        if not min_len <= len(author) <= max_len:
            raise ValueError(f'Expected author to have length between {min_len} and {max_len}, but it has length equal to {len(author)} instead')
        if re.fullmatch(self.author_pattern, author) is None:
            raise ValueError(f'Provided author value does not match pattern {self.author_pattern}')
        return author

    @validates('year_published')
    def validate_year_published(self, _, year_published):
        year_published = int(year_published)
        (min_value, max_value) = (500, 2500)
        if not min_value <= year_published <= max_value:
            raise ValueError(f'Expected year_published to be between {min_value} and {max_value}, but it is {year_published} instead')
        return year_published

    @validates('book_type')
    def validate_book_type(self, _, book_type):
        book_type = str(book_type)
        allowed_values = ['2days', '5days', '10days']
        if book_type not in allowed_values:
            raise ValueError(f'Invalid book type value {book_type}, expected one of [{", ".join(allowed_values)}]')
        return book_type


with app.app_context():
    db.create_all()