import pytest
from datetime import date
from project import db
from project import app as flask_app
from project.loans.models import Loan
from project.books.models import Book
from project.customers.models import Customer

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with flask_app.test_client() as client:
        with flask_app.app_context():
            db.create_all()
            yield client
            db.drop_all()

@pytest.fixture
def setup_book_and_customer():
    """Tworzy testową książkę ze statusem available oraz klienta w bazie."""
    book = Book(name='W pustyni i w puszczy', author='Henryk Sienkiewicz', year_published=1911, book_type='Powieść', status='available')
    customer = Customer(name='Jan Kowalski', city='Warszawa', age=30)
    db.session.add(book)
    db.session.add(customer)
    db.session.commit()

# --- SCENARIUSZ 1: TWORZENIE WYPOŻYCZENIA - WARIANT POPRAWNY ---
def test_create_loan_valid_input(client, setup_book_and_customer):
    """Testuje poprawne utworzenie wypożyczenia bezpiecznymi danymi."""
    response = client.post('/loans/create', data={
        'customer_name': 'Jan Kowalski',
        'book_name': 'W pustyni i w puszczy',
        'loan_date': date.today().strftime('%Y-%m-%d'),
        'return_date': date.today().strftime('%Y-%m-%d')
    })
    
    assert response.status_code in [200, 302]
    loan = Loan.query.filter_by(customer_name='Jan Kowalski').first()
    assert loan is not None
    assert loan.book_name == 'W pustyni i w puszczy'
    
    # Sprawdzamy, czy wypożyczona książka zniknęła z głównej tabeli books
    book = Book.query.filter_by(name='W pustyni i w puszczy').first()
    assert book is None

# --- SCENARIUSZ 2A: TWORZENIE WYPOŻYCZENIA - XSS W POLU CUSTOMER_NAME ---
def test_create_loan_invalid_xss_in_customer_name(client, setup_book_and_customer):
    """Testuje odrzucenie payloadu XSS w polu customer_name podczas wypożyczenia."""
    response = client.post('/loans/create', data={
        'customer_name': '<img src=x onerror=alert(1)>',
        'book_name': 'W pustyni i w puszczy',
        'loan_date': date.today().strftime('%Y-%m-%d'),
        'return_date': date.today().strftime('%Y-%m-%d')
    })
    
    # Wartość z tagami po oczyszczeniu przez sanitize_input staje się pusta,
    # co powoduje brak dostępnej książki / błąd braku dopasowania lub odrzucenie
    assert response.status_code in [400, 500]
    assert Loan.query.count() == 0

# --- SCENARIUSZ 2B: TWORZENIE WYPOŻYCZENIA - XSS W POLU BOOK_NAME ---
def test_create_loan_invalid_xss_in_book_name(client, setup_book_and_customer):
    """Testuje odrzucenie payloadu XSS w polu book_name podczas wypożyczenia."""
    response = client.post('/loans/create', data={
        'customer_name': 'Jan Kowalski',
        'book_name': '<img src=x onerror=alert(1)>',
        'loan_date': date.today().strftime('%Y-%m-%d'),
        'return_date': date.today().strftime('%Y-%m-%d')
    })
    
    # Książka o takiej nazwie nie istnieje, więc aplikacja zwraca błąd 400 (Book not available)
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert Loan.query.count() == 0