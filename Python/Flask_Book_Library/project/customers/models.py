from project import db, app
import html
import re

def sanitize_input(text):
    if not text:
        return ''
    if re.search(r'<|>|javascript:|on\w+=', text, re.IGNORECASE):
        cleaned = html.escape(text)
    cleaned = cleaned.replace('<', '').replace('>', '')
    return cleaned.strip()


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
