from project import db, app
import re


CUSTOMER_NAME_REGEX = re.compile(r"^[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ .\-]{1,64}$")
CITY_NAME_REGEX = re.compile(r"^[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ .\-]{1,64}$")
MIN_AGE = 1
MAX_AGE = 120


# Customer model
class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    city = db.Column(db.String(64))
    age = db.Column(db.Integer)

    @staticmethod
    def validate_name(name):
        if not isinstance(name, str) or not CUSTOMER_NAME_REGEX.match(name):
            raise ValueError(
                "Invalid customer name: must be 1-64 characters and contain only letters, spaces, dots, and hyphens."
            )
        return name

    @staticmethod
    def validate_city(city):
        if not isinstance(city, str) or not CITY_NAME_REGEX.match(city):
            raise ValueError(
                "Invalid city name: must be 1-64 characters and contain only letters, spaces, dots, and hyphens."
            )
        return city

    @staticmethod
    def validate_age(age):
        if isinstance(age, bool):
            raise ValueError("Invalid age: boolean is not allowed.")
        if isinstance(age, str):
            if not re.match(r"^\d+$", age):
                raise ValueError("Invalid age: must be a valid integer.")
            age = int(age)
        if not isinstance(age, int) or not (MIN_AGE <= age <= MAX_AGE):
            raise ValueError(f"Invalid age: must be an integer between {MIN_AGE} and {MAX_AGE}.")
        return age

    def __init__(self, name, city, age):
        self.name = self.validate_name(name)
        self.city = self.validate_city(city)
        self.age = self.validate_age(age)

    def __repr__(self):
        return f"Customer(ID: {self.id}, Name: {self.name}, City: {self.city}, Age: {self.age})"


with app.app_context():
    db.create_all()

