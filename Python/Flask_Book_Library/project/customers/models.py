import re

from sqlalchemy.orm import validates

from project import db, app


# Customer model
class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    city = db.Column(db.String(64))
    age = db.Column(db.Integer)

    def __init__(self, name, city, age):
        self.name = name
        self.city = city
        self.age = age

    def __repr__(self):
        return f"Customer(ID: {self.id}, Name: {self.name}, City: {self.city}, Age: {self.age})"
    max_len = 64
    pattern = '^[a-zA-Z0-9\s-]*$'

    @validates('name', 'city')
    def validate(self, key, value):
        if len(value) > self.max_len:
            raise ValueError(f"{key.capitalize()} is too long!")
        if not re.match(self.pattern, value):
            raise ValueError(f"{key.capitalize()} has invalid characters.")
        return value

with app.app_context():
    db.create_all()
