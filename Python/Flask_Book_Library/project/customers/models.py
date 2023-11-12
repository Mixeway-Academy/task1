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
        self._validate_input_value(name)
        self._validate_input_value(city)

        self.name = name
        self.city = city
        self.age = age

    def __repr__(self):
        return f"Customer(ID: {self.id}, Name: {self.name}, City: {self.city}, Age: {self.age})"
    
    def _validate_input_value(self, value):
        if not re.match("^[a-zA-Z ]{1,50}$", value):
            raise ValueError("Name and city must both contain only letters and be at most 50 characters long.")


with app.app_context():
    db.create_all()
