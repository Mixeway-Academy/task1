from project import db, app
import re
from sqlalchemy.orm import validates

# blocks building HTML/JS tags (stored XSS).
TEXT_PATTERN = re.compile(r"^[\w\s.,:;!?'\"()\-]+$", re.UNICODE)
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
    def validate_text(self, key, value):
        if isinstance(value, str):
            value = re.sub(r"\s+", " ", value.strip())
        if not isinstance(value, str) or not 1 <= len(value) <= 64 or not TEXT_PATTERN.match(value):
            raise ValueError(f"Field '{key}' contains characters that are not allowed")
        return value

    def __repr__(self):
        return f"Customer(ID: {self.id}, Name: {self.name}, City: {self.city}, Age: {self.age})"


with app.app_context():
    db.create_all()
