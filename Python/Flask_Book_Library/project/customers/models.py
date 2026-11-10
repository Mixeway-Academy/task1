from project import db, app
from sqlalchemy.orm import validates
import re

NAME_CITY_REGEX = re.compile(r"^[^\W\d_](?:[^\W\d_]|\s|[.,'\-]){0,63}$")


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

    @validates('name', 'city')
    def validate_text_fields(self, key, value):
        if not isinstance(value, str) or not NAME_CITY_REGEX.match(value.strip()):
            raise ValueError(f"Invalid customer {key}")
        return value.strip()

    def __repr__(self):
        return f"Customer(ID: {self.id}, Name: {self.name}, City: {self.city}, Age: {self.age})"


with app.app_context():
    db.create_all()
