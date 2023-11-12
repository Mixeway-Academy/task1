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
        self.name = name
        self.city = city
        self.age = age

    def _update_name(self, new_name):
        self._validate_name(new_name)
        self.name = new_name

    def _update_city(self, new_city):
        self._validate_city(new_city)
        self.city = new_city

    def _validate_name(self, name):
        if not re.fullmatch(r'[a-zA-Z ]{1,64}', name):
            raise ValueError('Customer name must not be longer than 64 characters or contain numbers or special characters')

    def _validate_city(self, city):
        if not re.fullmatch(r'[a-zA-Z ]{1,64}', city):
            raise ValueError('City name must not be longer than 64 characters or contain numbers or special characters')

    def __repr__(self):
        return f"Customer(ID: {self.id}, Name: {self.name}, City: {self.city}, Age: {self.age})"


with app.app_context():
    db.create_all()
