from project import db, app
import re
from sqlalchemy.orm import validates


# Customer model
class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    city = db.Column(db.String(64))
    age = db.Column(db.Integer)

    name_pattern = re.compile('^[a-z \'"-]{1,64}$', re.IGNORECASE)
    city_pattern = re.compile('^[a-z \'"-]{1,64}$', re.IGNORECASE)

    def __init__(self, name, city, age):
        self.name = name
        self.city = city
        self.age = age

    def __repr__(self):
        return f"Customer(ID: {self.id}, Name: {self.name}, City: {self.city}, Age: {self.age})"

    @validates('name')
    def validate_name(self, _, name):
        name = str(name)
        (min_len, max_len) = (1, 64)
        if not min_len <= len(name) <= max_len:
            raise ValueError(f'Expected name to have length between {min_len} and {max_len}, but it has length equal to {len(name)} instead')
        if re.fullmatch(self.name_pattern, name) is None:
            raise ValueError(f'Provided name value does not match pattern {self.name_pattern}')
        return name

    @validates('city')
    def validate_city(self, _, city):
        city = str(city)
        (min_len, max_len) = (1, 64)
        if not min_len <= len(city) <= max_len:
            raise ValueError(f'Expected city to have length between {min_len} and {max_len}, but it has length equal to {len(city)} instead')
        if re.fullmatch(self.city_pattern, city) is None:
            raise ValueError(f'Provided city value does not match pattern {self.city_pattern}')
        return city

    @validates('age')
    def validate_age(self, _, age):
        age = int(age)
        (min_value, max_value) = (0, 200)
        if not min_value <= age <= max_value:
            raise ValueError(f'Expected age to be between {min_value} and {max_value}, but it is {age} instead')
        return age


with app.app_context():
    db.create_all()
