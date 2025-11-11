from project import db, app
import re
import bleach


def _clean_text(value: str, field_name: str, max_len: int = 64, allow_digits: bool = True) -> str:
    if value is None:
        raise ValueError(f"{field_name} is required")

    original = str(value).strip()
    
    cleaned = bleach.clean(original, tags=[], attributes={}, strip=True).strip()

    if original != cleaned:
        raise ValueError(f"{field_name} cannot contain HTML or script tags")

    if not cleaned:
        raise ValueError(f"{field_name} cannot be empty after sanitization")
    if len(cleaned) > max_len:
        raise ValueError(f"{field_name} too long (max {max_len})")

    if allow_digits:
        pattern = r"^[A-Za-zĄąĆćĘęŁłŃńÓóŚśŹźŻż0-9\s'\-\.]+$"
    else:
        pattern = r"^[A-Za-zĄąĆćĘęŁłŃńÓóŚśŹźŻż\s'\-\.]+$"

    if not re.match(pattern, cleaned):
        raise ValueError(f"{field_name} can only contain letters, digits, spaces, '-', '.', and apostrophes")

    return cleaned



class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True, nullable=False)
    author = db.Column(db.String(64), nullable=False)
    year_published = db.Column(db.Integer, nullable=False)
    book_type = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default='available')

    def __init__(self, name, author, year_published, book_type, status='available'):
        self.name = _clean_text(name, "Book name", allow_digits=True)
        self.author = _clean_text(author, "Author", allow_digits=False)
        self.year_published = year_published
        self.book_type = _clean_text(book_type, "Book type")
        self.status = _clean_text(status, "Status")

    def __repr__(self):
        return (f"Book(ID: {self.id}, Name: {self.name}, Author: {self.author}, "
                f"Year Published: {self.year_published}, Type: {self.book_type}, Status: {self.status})")


with app.app_context():
    db.create_all()