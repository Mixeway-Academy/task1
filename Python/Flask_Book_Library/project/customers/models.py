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
        if len(name) < 3 and len(name) > 64:
            raise ValueError('Name should have length between 3 and 64 characters!')
        if re.fullmatch(r'[\w\s:\-,]{3,64}', name) is None:
            raise ValueError('Inappropriate symbol used: Name should contain only letters, digits, spaces, hyphens, commas and colons!')
        self.name = name
        if len(city) < 3 and len(city) > 64:
            raise ValueError('City should have length between 3 and 64 characters!')
        if re.fullmatch(r'[\w\s:\-,]{3,64}', city) is None:
            raise ValueError('Inappropriate symbol used: City should contain only letters, digits, spaces, hyphens, commas and colons!')
        self.city = city
        self.age = age

    def __repr__(self):
        return f"Customer(ID: {self.id}, Name: {self.name}, City: {self.city}, Age: {self.age})"


with app.app_context():
    db.create_all()
