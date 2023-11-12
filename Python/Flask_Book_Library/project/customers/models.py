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
    def validate_name(self, _, value):
        regex = r"^[A-Za-z\s]*$"

        if not re.match(regex, value):
            raise ValueError("The only allowed characters in \"Name\" field are: alphabetic characters, spaces")
        return value

    @validates('city')
    def validate_city(self, _, value):
        regex = r"^[A-Za-z\s]*$"

        if not re.match(regex, value):
            raise ValueError("The only allowed characters in \"City\" field are: alphabetic characters, spaces")
        return value


with app.app_context():
    db.create_all()
