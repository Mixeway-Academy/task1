from project import db, app
import re


class BookChecker:
    """
    A class used to validate book information.
    Methods
    -------
    check_xss(name: str) -> bool
        Checks if the given string contains any characters that could be used for XSS attacks.
    check_name(name: str) -> bool
        Validates the book name to ensure it contains only letters, numbers, and spaces.
    check_author(author: str) -> bool
        Validates the author's name to ensure it contains only letters and spaces.
    check_year_published(year_published: str) -> bool
        Validates the year published to ensure it contains only numbers.
    check_book(book: Book) -> bool
        Validates the entire book object by checking its name, author, and year published.
    """

    name_maxsize = 64
    author_maxsize = 64
    age_maxsize = 16
    book_types = [('2days', 'Up to 2 days'), ('5days', 'Up to 5 days'), ('10days', 'Up to 10 days')]

    def check_xss(self, name):
        if re.match(r"[<>\"\'&]", name):
            raise ValueError("Name must not contain any of the following characters: <, >, \", ', &")
        return True

    def check_name(self, name):
        self.check_xss(name)
        if re.match(r"^[a-zA-Z0-9\s]+$", name) and len(name) <= self.name_maxsize:
            return True

        raise ValueError("Name must contain only letters, numbers and spaces")

    def check_author(self, author):
        self.check_xss(author)
        if re.match(r"^[a-zA-Z\s]+$", author) and len(author) <= self.author_maxsize:
            return True

        raise ValueError("Author must contain only letters and spaces")

    def check_year_published(self, year_published):
        year_published = str(year_published) # for len() to work
        self.check_xss(year_published)
        if re.match(r"^[0-9]+$", year_published) and len(year_published) < self.age_maxsize:
            return True

        raise ValueError("Year Published must contain only numbers")
    
    def check_book_type(self, book_type):
        self.check_xss(book_type)
        search_types = [t[0] for t in self.book_types]
        if book_type in search_types:
            return True
        raise ValueError("Book type is invalid")
    
    def check_book(self, book):
        if (
            self.check_name(book.name)
            and self.check_author(book.author)
            and self.check_year_published(book.year_published)
        ):
            return True
        raise ValueError("Book data is invalid")

checker = BookChecker()

# Book model
class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(checker.name_maxsize), unique=True, index=True)
    author = db.Column(db.String(checker.author_maxsize))
    year_published = db.Column(db.Integer)
    book_type = db.Column(db.String(20))
    status = db.Column(db.String(20), default="available")

    def __init__(self, name, author, year_published, book_type, status="available"):
        print(f'{name=} {author=} {year_published=} {book_type=} {status=}')
        self.name = name if checker.check_name(name) else None
        self.author = author if checker.check_author(author) else None
        self.year_published = year_published if checker.check_year_published(year_published) else None
        self.book_type = book_type if checker.check_book_type(book_type) else None
        self.status = status if checker.check_name(status) else None

    def __repr__(self):
        return f"Book(ID: {self.id}, Name: {self.name}, Author: {self.author}, Year Published: {self.year_published}, Type: {self.book_type}, Status: {self.status})"


with app.app_context():
    db.create_all()
