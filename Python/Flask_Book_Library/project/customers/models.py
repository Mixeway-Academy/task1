from project import db, app
from project.check_text import check_text
from sqlalchemy.orm import validates


# Customer model
class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    city = db.Column(db.String(64))
    age = db.Column(db.Integer)

    def __init__(self, name, city, age):
        self.name = name
        self.city = city
        self.age = age

    @validates('name', 'city')
    def validate_text_fields(self, key, value):
        return check_text(value, max_len=64)

    def __repr__(self):
        return f"Customer(ID: {self.id}, Name: {self.name}, City: {self.city}, Age: {self.age})"


with app.app_context():
    db.create_all()
