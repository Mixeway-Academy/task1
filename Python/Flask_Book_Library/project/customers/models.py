from project import db, app
from markupsafe import escape
import re


# Customer model
class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    city = db.Column(db.String(64))
    age = db.Column(db.Integer)

    def __init__(self, name, city, age):
        # na potrzeby weryfikacji w zadaniu funkcja escape jest używana tylko wtedy gdy wykryte są specjalne znaki
        if self.contains_special_chars(name):
            self.name = escape(name)
        else:
            self.name = name

        if self.contains_special_chars(city):
            self.city = escape(city)
        else:
            self.city = city
        self.age = age

    @staticmethod
    def contains_special_chars(value: str) -> bool:
        """
        Sprawdzenie, czy w stringu są znaki specjalne sugerujące wstrzyknięcie.
        """
        return bool(re.search(r"[<>&\"'/-;]", value))
    def __repr__(self):
        return f"Customer(ID: {self.id}, Name: {self.name}, City: {self.city}, Age: {self.age})"


with app.app_context():
    db.create_all()
