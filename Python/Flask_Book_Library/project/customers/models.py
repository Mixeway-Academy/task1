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
    
        if not re.match(r'^[a-zA-Z-]+$', name) or not (1 <= len(name) <= 64):
            raise ValueError(400, "Niepoprawna nazwa klienta. Dozwolone są znaki alfabetyczne i myślnik.")

        if not re.match(r'^[a-zA-Z]+$', city) or not (1 <= len(city) <= 64):
            raise ValueError(400, "Niepoprawna nazwa miasta. Dozwolone są znaki alfabetyczne.")
            
        self.name = name
        self.city = city
        self.age = age

    def __repr__(self):
        return f"Customer(ID: {self.id}, Name: {self.name}, City: {self.city}, Age: {self.age})"


with app.app_context():
    db.create_all()
