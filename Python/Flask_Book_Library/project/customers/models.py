from project import db, app
from sqlalchemy.orm import validates
import re


# Customer model
class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    city = db.Column(db.String(64))
    age = db.Column(db.Integer)

    VALID_NAME_PATTERN = r'^[a-zA-Z\s\.-]*$'
    VALID_CITY_PATTERN = r'^[a-zA-Z\s,\.-]*$'
    max_len = 64

    @validates('name', 'city')
    def validate_name_and_city(self, key, value):
        if len(value) > self.max_len:
            raise ValueError(f"{key.capitalize()} too long.")
        pattern = self.VALID_NAME_PATTERN if key == 'name' else self.VALID_CITY_PATTERN
        if not re.match(pattern, value):
            raise ValueError(f"{key.capitalize()} contains invalid characters.")
        return value

    def __init__(self, name, city, age):
        self.name = name
        self.city = city
        self.age = age

    def __repr__(self):
        return f"Customer(ID: {self.id}, Name: {self.name}, City: {self.city}, Age: {self.age})"


with app.app_context():
    db.create_all()
