from project import db, app
import re
from sqlalchemy.orm import validates

CHAR_NAME = re.compile(r'^[A-Za-zĄąĆćĘęŁłŃńÓóŚśŹźŻż \.\-]{1,80}$')
CHAR_CITY = re.compile(r'^[A-Za-zĄąĆćĘęŁłŃńÓóŚśŹźŻż \.\-]{1,50}$')

# Customer model
class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    city = db.Column(db.String(64))
    age = db.Column(db.Integer)

    @validates('name')
    def validate_name(self, key, name):
        if not name or not CHAR_NAME.match(name):
            raise ValueError("Invalid customer name.")
        return name

    @validates('city')
    def validate_city(self, key, city):
        if not city or not CHAR_CITY.match(city):
            raise ValueError("Invalid city.")
        return city
        
    def __init__(self, name, city, age):
        self.name = name
        self.city = city
        self.age = age

    def __repr__(self):
        return f"Customer(ID: {self.id}, Name: {self.name}, City: {self.city}, Age: {self.age})"

with app.app_context():
    db.create_all()