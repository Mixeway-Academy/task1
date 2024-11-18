from project import db, app
import re

class CustomerChecker:
    name_maxsize = 64
    city_maxsize = 64
    age_maxsize = 16

    def check_xss(self, name):
        if re.match(r'[<>\"\'&]', name):
            raise ValueError('Name must not contain any of the following characters: <, >, ", \', &')
        return True
    
    def check_name(self, name):
        self.check_xss(name)
        
        if re.match(r'^[a-zA-Z\s]+$', name) and len(name) <= self.name_maxsize:
            return True

        raise ValueError('Name must contain only letters and spaces')
    
    def check_city(self, city):
        return self.check_name(city)
    
    def check_age(self, age):
        age = str(age)
        self.check_xss(age)
        if re.match(r'^[0-9]+$', age) and len(age) <= self.age_maxsize:
            return True

        raise ValueError('Age must contain only numbers')
        
    def check_customer(self, customer):
        if (
            self.check_name(customer.name)
            and self.check_city(customer.city)
            and self.check_age(customer.age)
        ):
            return True
        raise ValueError('Customer data is invalid')

checker = CustomerChecker()

# Customer model
class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(checker.name_maxsize), unique=True, index=True)
    city = db.Column(db.String(checker.city_maxsize))
    age = db.Column(db.Integer)

    def __init__(self, name, city, age):
        
        self.name = name if checker.check_name(name) else None
        self.city = city if checker.check_city(city) else None
        self.age = age if checker.check_age(age) else None

    def __repr__(self):
        return f"Customer(ID: {self.id}, Name: {self.name}, City: {self.city}, Age: {self.age})"


with app.app_context():
    db.create_all()
