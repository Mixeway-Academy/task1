from project import db, app
import re


BOOK_NAME_REGEX = re.compile(r"^[a-zA-Z0-9ąćęłńóśźżĄĆĘŁŃÓŚŹŻ .,:\-]{1,64}$")
AUTHOR_NAME_REGEX = re.compile(r"^[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ .\-]{1,64}$")
ALLOWED_BOOK_TYPES = {'2days', '5days', '10days'}
ALLOWED_BOOK_STATUSES = {'available', 'loaned'}
MIN_YEAR_PUBLISHED = 1
MAX_YEAR_PUBLISHED = 2026


# Book model
class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    author = db.Column(db.String(64))
    year_published = db.Column(db.Integer)
    book_type = db.Column(db.String(20))
    status = db.Column(db.String(20), default='available')

    @staticmethod
    def validate_name(name):
        if not isinstance(name, str) or not BOOK_NAME_REGEX.match(name):
            raise ValueError(
                "Invalid book name: must be 1-64 characters and contain only letters, digits, spaces, and basic punctuation (.,:-)."
            )
        return name

    @staticmethod
    def validate_author(author):
        if not isinstance(author, str) or not AUTHOR_NAME_REGEX.match(author):
            raise ValueError(
                "Invalid author name: must be 1-64 characters and contain only letters, spaces, dots, and hyphens."
            )
        return author

    @staticmethod
    def validate_year_published(year_published):
        if isinstance(year_published, bool):
            raise ValueError("Invalid year_published: boolean is not allowed.")
        if isinstance(year_published, str):
            if not re.match(r"^\d+$", year_published):
                raise ValueError("Invalid year_published: must be a valid integer.")
            year_published = int(year_published)
        if not isinstance(year_published, int) or not (MIN_YEAR_PUBLISHED <= year_published <= MAX_YEAR_PUBLISHED):
            raise ValueError(
                f"Invalid year_published: must be an integer between {MIN_YEAR_PUBLISHED} and {MAX_YEAR_PUBLISHED}."
            )
        return year_published

    @staticmethod
    def validate_book_type(book_type):
        if not isinstance(book_type, str) or book_type not in ALLOWED_BOOK_TYPES:
            raise ValueError(f"Invalid book_type: must be one of {sorted(ALLOWED_BOOK_TYPES)}.")
        return book_type

    @staticmethod
    def validate_status(status):
        if not isinstance(status, str) or status not in ALLOWED_BOOK_STATUSES:
            raise ValueError(f"Invalid status: must be one of {sorted(ALLOWED_BOOK_STATUSES)}.")
        return status

    def __init__(self, name, author, year_published, book_type, status='available'):
        self.name = self.validate_name(name)
        self.author = self.validate_author(author)
        self.year_published = self.validate_year_published(year_published)
        self.book_type = self.validate_book_type(book_type)
        self.status = self.validate_status(status)

    def __repr__(self):
        return f"Book(ID: {self.id}, Name: {self.name}, Author: {self.author}, Year Published: {self.year_published}, Type: {self.book_type}, Status: {self.status})"


with app.app_context():
    db.create_all()
