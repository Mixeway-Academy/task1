from project import db, app
import re


# Customer model
class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    city = db.Column(db.String(64))
    age = db.Column(db.Integer)

    # Walidacja pola tekstowego za pomocą wyrażenia regularnego
    def validate_text(self, text):
        if not re.match("^[a-zA-Z0-9\s-]*$", text):
            raise ValueError("Dozwolone są tylko małe i wielkie litery, cyfry, spacja oraz myślnik.")
        return text

    def __init__(self, name, city, age):
        # Walidacja każdego z pól tekstowych
        self.name = self.validate_text(name)
        self.city = self.validate_text(city)
        self.age = age

    def __repr__(self):
        return f"Customer(ID: {self.id}, Name: {self.name}, City: {self.city}, Age: {self.age})"


with app.app_context():
    db.create_all()

