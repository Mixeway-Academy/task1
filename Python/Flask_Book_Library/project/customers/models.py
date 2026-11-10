from project import db, app
import re


# Customer model
class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True, nullable=False)
    city = db.Column(db.String(64), nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def __init__(self, name, city, age):
        self.name = self.validate_text(name, "Imię i nazwisko", 64)
        self.city = self.validate_text(city, "Miasto", 64)
        self.age = self.validate_age(age)

    @staticmethod
    def validate_text(value, field_name, max_length):
        """
        Walidacja pól tekstowych.
        """

        if not isinstance(value, str):
            raise ValueError(f"{field_name} musi być tekstem")

        value = value.strip()

        if not value:
            raise ValueError(f"{field_name} nie może być puste")

        if len(value) > max_length:
            raise ValueError(
                f"{field_name} może mieć maksymalnie {max_length} znaków"
            )

        # Blokowanie znaczników HTML mogących prowadzić do XSS
        if re.search(r"<[^>]*>", value):
            raise ValueError(
                f"{field_name} nie może zawierać znaczników HTML"
            )

        return value

    @staticmethod
    def validate_age(value):
        """
        Walidacja wieku klienta.
        """

        if isinstance(value, bool):
            raise ValueError("Wiek musi być liczbą całkowitą")

        try:
            age = int(value)
        except (ValueError, TypeError):
            raise ValueError("Wiek musi być liczbą całkowitą")

        if age < 18 or age > 120:
            raise ValueError("Wiek musi mieścić się w zakresie 18-120 lat")

        return age

    def __repr__(self):
        return (
            f"Customer(ID: {self.id}, Name: {self.name}, "
            f"City: {self.city}, Age: {self.age})"
        )


with app.app_context():
    db.create_all()
