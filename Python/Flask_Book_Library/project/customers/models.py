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

        if len(name) > 64:
            name = name[:64]
            #raise ValueError("Too long name.") #Można albo wywalać błąd, albo obcinać

        if  not re.match(r'^[A-Za-z\s-]*$', name): #Regex na litery małe, duże, spację i -
            raise ValueError("Name must contain only letters and spaces.") #Tutaj zamiast sanityzacji danych, walimy błędem
            #name = re.sub(r'[^A-Za-z\s-]', '', name) #Można też usunąć znaki niepasujące

        if len(city) > 64: #Dla polskiego systemu bibliotecznego można byłoby spokojnie dać granicę 40 znaków
            city = city[:64]
            #raise ValueError("Too long author.")

        if  not re.match(r'^[A-Za-z\s-]*$', city): #Regex na litery małe, duże, spację i -
            #raise ValueError("City must contain only letters and spaces.") #Tutaj zamiast sanityzacji danych, walimy błędem
            city = re.sub(r'[^A-Za-z\s-]', '', city) #Można też usunąć znaki niepasujące

        if (int(age) < 1 or int(age) > 120):
            raise ValueError("You're so funny. :)")

        self.name = name
        self.city = city
        self.age = age

    def __repr__(self):
        return f"Customer(ID: {self.id}, Name: {self.name}, City: {self.city}, Age: {self.age})"


with app.app_context():
    db.create_all()
