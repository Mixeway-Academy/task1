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
        if (len(name) < 1) or (len(name) > 100):
            raise ValueError("Customer name must contain 1-100 characters")
        if (len(city) < 1) or (len(city) > 60):
            raise ValueError("City must must contain 1-60 characters")
        if not re.match(r"^[a-zA-Z\s]+$", name):
            raise ValueError("Customer must only contain letters and spaces")
        if not re.match(r"^[a-zA-Z\s]+$", city):
            raise ValueError("City must only contain letters and spaces")

        self.name = name
        self.city = city
        self.age = age

    def __repr__(self):
        return f"Customer(ID: {self.id}, Name: {self.name}, City: {self.city}, Age: {self.age})"


with app.app_context():
    db.create_all()
