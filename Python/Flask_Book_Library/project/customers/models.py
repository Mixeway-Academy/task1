from project import db, app
import re

VALID_NAME = re.compile(r'^[A-Za-z0-9ĄąĆćĘęŁłŃńÓóŚśŹźŻż ]{1,100}$')
VALID_CITY = re.compile(r'^[A-Za-zĄąĆćĘęŁłŃńÓóŚśŹźŻż ]{1,80}$')

# Customer model
class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    city = db.Column(db.String(64))
    age = db.Column(db.Integer)

    def __init__(self, name, city, age):
        if not VALID_NAME.match(name):
            raise ValueError("Invalid customer name. Use only letters (including Polish), digits, and spaces (1–100 characters).") 
        if not VALID_CITY.match(city):
            raise ValueError("Invalid city name. Use only letters (including Polish), digits, and spaces (1–80 characters).")
        self.name = name
        self.city = city
        self.age = age

    def __repr__(self):
        return f"Customer(ID: {self.id}, Name: {self.name}, City: {self.city}, Age: {self.age})"


with app.app_context():
    db.create_all()
