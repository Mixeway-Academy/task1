from project import db, app
from markupsafe import escape
from sqlalchemy.ext.hybrid import hybrid_property

# Customer model
class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column("name", db.String(64), unique=True, index=True)
    _city = db.Column("city", db.String(64))
    age = db.Column(db.Integer)

    def __init__(self, name, city, age):
        self.name = name
        self.city = city
        self.age = age

    @hybrid_property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = escape(value)

    @name.expression
    def name(cls):
        return cls._name

    @hybrid_property
    def city(self):
        return self._city

    @city.setter
    def city(self, value):
        self._city = escape(value)

    @city.expression
    def city(cls):
        return cls._city

    def __repr__(self):
        return f"Customer(ID: {self.id}, Name: {self.name}, City: {self.city}, Age: {self.age})"


with app.app_context():
    db.create_all()
