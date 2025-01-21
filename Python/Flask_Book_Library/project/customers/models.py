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
        if(len(name)<1 or len(name)>64):
            raise ValueError("Invalid length of name string")
        if not (re.match(r"^[\w\-\s]+$", name)):
            raise ValueError("Unexpected characters in name string")
        self.name = name
        if(len(city)<1 or len(city)>64):
            raise ValueError("Invalid length of city string")
        if not (re.match(r"^[\w\-\s]+$", city)):
            raise ValueError("Unexpected characters in city string")
        self.city = city
        self.age = age

    def __repr__(self):
        return f"Customer(ID: {self.id}, Name: {self.name}, City: {self.city}, Age: {self.age})"


with app.app_context():
    db.create_all()
