from project import db, app


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

    def __repr__(self):
        return f"Customer(ID: {self.id}, Name: {self.name}, City: {self.city}, Age: {self.age})"

    def is_valid(self):
        if len(self.name) > 64:
            return False
        if len(self.city) > 64:
            return False
        if not self.age.isnumeric() or int(self.age) <= 0:
            return False
        return True

with app.app_context():
    db.create_all()
