import re
from project import db, app

# Customer model
class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    city = db.Column(db.String(64))
    age = db.Column(db.Integer)

    def __init__(self, name, city, age):
        if len(name) < 5 or len(name) > 50:
            raise ValueError('Name must be between 5 and 50 characters')
        if len(city) < 3 or len(city) > 50:
            raise ValueError('City must be between 3 and 50 characters')
        if name and not re.match("^[a-zA-Z ]*$", name):
            raise ValueError('Name must contain only letters and spaces')
        if city and not re.match("^[a-zA-Z]*$", city):
            raise ValueError('City must contain only letters')
        self.name = name
        self.city = city
        self.age = age

    def __repr__(self):
        return f"Customer(ID: {self.id}, Name: {self.name}, City: {self.city}, Age: {self.age})"


with app.app_context():
    db.create_all()
