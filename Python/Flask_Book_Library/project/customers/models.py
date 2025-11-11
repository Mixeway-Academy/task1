import bleach
import re
from project import db, app


def _clean_text(value: str, field_name: str, max_len: int = 64, letters_only: bool = False) -> str:
    if value is None:
        raise ValueError(f"{field_name} is required")

    cleaned = bleach.clean(str(value), tags=[], attributes={}, strip=True).strip()

    if not cleaned:
        raise ValueError(f"{field_name} cannot be empty after sanitization")
    if len(cleaned) > max_len:
        raise ValueError(f"{field_name} too long (max {max_len})")

    if letters_only and not re.match(r"^[A-Za-zÀ-ž\s-]+$", cleaned):
        raise ValueError(f"{field_name} may only contain letters, spaces, or hyphens")

    return cleaned

def _validate_age(value) -> int:
    try:
        age_int = int(value)
    except (TypeError, ValueError):
        raise ValueError("Age must be an integer")
    if age_int < 0 or age_int > 150:
        raise ValueError("Age out of allowed range (0-150)")
    return age_int

class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    city = db.Column(db.String(64))
    age = db.Column(db.Integer)

    def __init__(self, name, city, age):
        self.name = _clean_text(name, "Name", letters_only=True)
        self.city = _clean_text(city, "City", letters_only=True)
        self.age = _validate_age(age)


    def __repr__(self):
        return f"Customer(ID: {self.id}, Name: {self.name}, City: {self.city}, Age: {self.age})"


with app.app_context():
    db.create_all()
