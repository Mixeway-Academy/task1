from project import db, app
from project.core.rules import WordCountBetween, OnlyTextRegex
import re


# Customer model
class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    city = db.Column(db.String(64))
    age = db.Column(db.Integer)

    def __init__(self, name, city, age):
        WordCountBetween(name, 2, 30, field='name')
        WordCountBetween(city, 2, 30, field='city')
        OnlyTextRegex(name, field='name')
        OnlyTextRegex(city, field='city')
        self.name = name
        self.city = city
        self.age = age

    def __repr__(self):
        return f"Customer(ID: {self.id}, Name: {self.name}, City: {self.city}, Age: {self.age})"


with app.app_context():
    db.create_all()
