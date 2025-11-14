from project import db, app
from project.constants import (
    AUTHOR_NAME_RE, 
    CITY_RE,
    MAX_NAME_OR_AUTHOR_LENGTH, 
    MAX_CITY_LENGTH
)

# Customer model
class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(MAX_NAME_OR_AUTHOR_LENGTH), unique=True, index=True)
    city = db.Column(db.String(MAX_CITY_LENGTH))
    age = db.Column(db.Integer)

    def __init__(self, name, city, age):
        name = name.strip()
        city = city.strip()
        
        if len(name) > MAX_NAME_OR_AUTHOR_LENGTH or not AUTHOR_NAME_RE.fullmatch(name):
            raise ValueError("Invalid customer name format or length.")
        
        if len(city) > MAX_CITY_LENGTH or not CITY_RE.fullmatch(city):
            raise ValueError("Invalid city name format or length.")
        
        if not isinstance(age, int) or age < 0 or age > 120:
            raise ValueError("Invalid age. Must be an integer between 0 and 120.")
        
        self.name = name
        self.city = city
        self.age = age

    def __repr__(self):
        return f"Customer(ID: {self.id}, Name: {self.name}, City: {self.city}, Age: {self.age})"


with app.app_context():
    db.create_all()
