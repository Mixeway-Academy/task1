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

    def __init__(self, name, city, age):
        self.name = name
        self.city = city
        self.age = age

    def __repr__(self):
        return f"Customer(ID: {self.id}, Name: {self.name}, City: {self.city}, Age: {self.age})"

    @validates('name')
    def name_validator(self, key, value):
        if not value:
            raise ValueError("Name must not be blank")
        if re.match(r'^[a-zA-Z ]+$', value) is None:
            raise ValueError("Name must contain only letters and spaces")
        return value

    @validates("city")
    def city_validator(self, key, value):
        if not value:
            raise ValueError("City must not be blank")
        if re.match(r'^[a-zA-Z ]+$', value) is None:
            raise ValueError("City must contain only letters and spaces")
        return value


with app.app_context():
    db.create_all()
