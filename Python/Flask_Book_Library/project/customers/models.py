from project import db, app
import re


# Customer model
class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    city = db.Column(db.String(64))
    age = db.Column(db.Integer)

    def __init__(self, name, city, age):
        if len(name) < 1 or len(name) > 255:
            raise ValueError('Name must have between 1-255 characters')
        if len(city) < 1 or len(city) > 255:
            raise ValueError('City must have between 1-255 characters')
        if name is None or not re.match("^[\w\d .\'\"()&!@#$%*;:_-]+$", name):
            raise ValueError('Name contains invalid characters or is empty')
        if city is None or not re.match("^[\w .-]+$", city):
            raise ValueError('City contains invalid characters or is empty')
        if int(age) < 1:
            raise ValueError('Age must be greater than or equal to 1')
        self.name = name
        self.city = city
        self.age = age

    def __repr__(self):
        return f"Customer(ID: {self.id}, Name: {self.name}, City: {self.city}, Age: {self.age})"


with app.app_context():
    db.create_all()
