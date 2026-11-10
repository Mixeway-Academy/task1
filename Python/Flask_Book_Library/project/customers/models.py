from project import db, app
import re


# Whitelist: letters, digits, spaces and basic punctuation only (blocks HTML/JS)
CUSTOMER_TEXT_RE = re.compile(r'^[A-Za-z0-9ĄąĆćĘęŁłŃńÓóŚśŹźŻż .,\-]{1,64}$')


def validate_customer_text(value, field_name):
    if not isinstance(value, str) or not CUSTOMER_TEXT_RE.match(value):
        raise ValueError(
            f'Invalid {field_name}: only letters, digits, spaces and .,- are allowed (max 64 chars)'
        )


# Customer model
class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    city = db.Column(db.String(64))
    age = db.Column(db.Integer)

    def __init__(self, name, city, age):
        validate_customer_text(name, 'name')
        validate_customer_text(city, 'city')
        self.name = name
        self.city = city
        self.age = age

    def __repr__(self):
        return f"Customer(ID: {self.id}, Name: {self.name}, City: {self.city}, Age: {self.age})"


with app.app_context():
    db.create_all()
