from project import db, app
import re


# Book model
class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    author = db.Column(db.String(64))
    year_published = db.Column(db.Integer)
    book_type = db.Column(db.String(20))
    status = db.Column(db.String(20), default='available')

    def __init__(self, name, author, year_published, book_type, status='available'):

        if len(name) > 64:
            name = name[:64]
            #raise ValueError("Too long name.") #Można albo wywalać błąd, albo obcinać

        if not re.match(r'^[A-Za-z0-9\s!@#$%&*_\-+=,.:;\'"€]*$', name): #Regex matchujący litery, cyfry, spację i znaki, które mogą się znaleźć w tytułach 'niszowych(?)', np. $, € w ekonomii
            #raise ValueError("Invalid characters in Name.") #Można rzucić błędem
            name = re.sub(r'[^A-Za-z0-9\s!@#$%&*_\-+=,.:;\'"€]', '', name) #Można też usunąć znaki niepasujące

        if len(author) > 64:
            name = name[:64]
            #raise ValueError("Too long author.")

        if  not re.match(r'^[A-Za-z\s-]*$', author): #Regex na litery małe, duże, spację i -
            raise ValueError("Author name must contain only letters and spaces.") #Tutaj zamiast sanityzacji danych, walimy błędem
            #author = re.sub(r'[^A-Za-z\s-]', '', author) #Można też usunąć znaki niepasujące

        #year_published przyjmuje kosmiczne wartości, ale tylko integer, więc nie ma zagrożenia XSS z użyciem tego pola

        self.name = name
        self.author = author
        self.year_published = year_published
        self.book_type = book_type
        self.status = status

    def __repr__(self):
        return f"Book(ID: {self.id}, Name: {self.name}, Author: {self.author}, Year Published: {self.year_published}, Type: {self.book_type}, Status: {self.status})"


with app.app_context():
    db.create_all()
