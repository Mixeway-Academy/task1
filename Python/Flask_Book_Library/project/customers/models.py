from project import db, app
import re
import html


# Customer model
class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    city = db.Column(db.String(64))
    age = db.Column(db.Integer)

    def __init__(self, name, city, age):
        self.name = self._sanitize_input(name)
        self.city = self._sanitize_input(city)
        self.age = age
    
    def _sanitize_input(self, value):
        """Remove HTML/JS tags and escape dangerous characters"""
        if not value:
            return value
        # Remove script tags and escape HTML
        value = re.sub(r'<script[^>]*>.*?</script>', '', str(value), flags=re.IGNORECASE | re.DOTALL)
        value = html.escape(value)
        return value

    def __repr__(self):
        return f"Customer(ID: {self.id}, Name: {self.name}, City: {self.city}, Age: {self.age})"


with app.app_context():
    db.create_all()
