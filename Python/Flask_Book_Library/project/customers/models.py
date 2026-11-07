from project import db, app
from project.validators.text_validator import validate_text


# Customer model
class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    city = db.Column(db.String(64))
    age = db.Column(db.Integer)

    def __init__(self, name, city, age):
        self.name = validate_text(name)
        self.city = validate_text(city)
        self.age = age

    def validate(self):
        self.name = validate_text(self.name)
        self.city = validate_text(self.city)

    def __repr__(self):
        return f"Customer(ID: {self.id}, Name: {self.name}, City: {self.city}, Age: {self.age})"


with app.app_context():
    db.create_all()
