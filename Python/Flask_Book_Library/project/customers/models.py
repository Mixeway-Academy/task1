from project import db, app
import html
import re
import unicodedata


def sanitize_input(value: str, max_length: int = 64) -> str:
    if not isinstance(value, str):
        raise ValueError("Wartość musi być tekstem")

    value = unicodedata.normalize('NFC', value.strip())

    if re.search(r'<|>|javascript:|on\w+=', value, re.IGNORECASE):
        value = html.escape(value)

    if len(value) > max_length:
        value = value[:max_length]

    return value


# Customer model
class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    city = db.Column(db.String(64))
    age = db.Column(db.Integer)

    def __init__(self, name, city, age):
        self.name = sanitize_input(name)
        self.city = sanitize_input(city)
        self.age = age

    def __repr__(self):
        return f"Customer(ID: {self.id}, Name: {self.name}, City: {self.city}, Age: {self.age})"


with app.app_context():
    db.create_all()
