from project import db, app

# Model Klienta
class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    city = db.Column(db.String(64))
    age = db.Column(db.Integer)

    def __init__(self, name, city, age):
        # Walidacja nazwy
        if not 1 <= len(name) <= 64:
            raise ValueError("Nazwa musi mieć od 1 do 64 znaków.")
        
        if any(char in "!@#$%^&*()_+=[]{};:'\"<>,./?\\|" for char in name):
            raise ValueError("Nazwa zawiera niedozwolone znaki.")

        # Walidacja miasta
        if not 1 <= len(city) <= 64:
            raise ValueError("Nazwa miasta musi mieć od 1 do 64 znaków.")
        
        if any(char in "!@#$%^&*()_+=[]{};:'\"<>,./?\\|" for char in city):
            raise ValueError("Nazwa miasta zawiera niedozwolone znaki.")

        self.name = name
        self.city = city
        self.age = age

    def __repr__(self):
        return f"Customer(ID: {self.id}, Name: {self.name}, City: {self.city}, Age: {self.age})"


with app.app_context():
    db.create_all()
