import pytest
from project import db
from project import app as flask_app
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

# --- SCENARIUSZ 1: TWORZENIE - WARIANT POPRAWNY ---
def test_create_customer_valid_input(client):
    """Testuje poprawne dodanie klienta bez niedozwolonych tagów HTML."""
    response = client.post('/customers/create', data={
        'name': 'Jan Kowalski',
        'city': 'Warszawa',
        'age': 30
    })
    
    assert response.status_code in [200, 302]
    customer = Customer.query.filter_by(name='Jan Kowalski').first()
    assert customer is not None
    assert customer.city == 'Warszawa'

# --- SCENARIUSZ 2A: TWORZENIE - XSS W POLU NAME ---
def test_create_customer_invalid_xss_in_name(client):
    """Testuje odrzucenie payloadu w polu name przy tworzeniu klienta."""
    response = client.post('/customers/create', data={
        'name': '<img src=x onerror=alert(1)>',
        'city': 'Warszawa',
        'age': 30
    })
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert Customer.query.count() == 0

# --- SCENARIUSZ 2B: TWORZENIE - XSS W POLU CITY ---
def test_create_customer_invalid_xss_in_city(client):
    """Testuje odrzucenie payloadu w polu city przy tworzeniu klienta."""
    response = client.post('/customers/create', data={
        'name': 'Jan Kowalski',
        'city': '<img src=x onerror=alert(1)>',
        'age': 30
    })
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert Customer.query.count() == 0

# --- SCENARIUSZ 3: EDYCJA - WARIANT POPRAWNY ---
def test_edit_customer_valid_input(client):
    """Testuje poprawną edycję istniejącego klienta bezpiecznymi danymi."""
    with client.application.app_context():
        customer = Customer(name='Stare imie', city='Kraków', age=25)
        db.session.add(customer)
        db.session.commit()
        customer_id = customer.id

    response = client.post(f'/customers/{customer_id}/edit', data={
        'name': 'Nowe imie',
        'city': 'Gdańsk',
        'age': 26
    })

    assert response.status_code in [200, 302]

    with client.application.app_context():
        updated_customer = Customer.query.get(customer_id)
        assert updated_customer.name == 'Nowe imie'
        assert updated_customer.city == 'Gdańsk'

# --- SCENARIUSZ 4A: EDYCJA - XSS W POLU NAME ---
def test_edit_customer_invalid_xss_in_name(client):
    """Testuje odrzucenie próby wstrzyknięcia payloadu w polu name podczas edycji klienta."""
    with client.application.app_context():
        customer = Customer(name='Bezpieczny Klient', city='Warszawa', age=30)
        db.session.add(customer)
        db.session.commit()
        customer_id = customer.id

    response = client.post(f'/customers/{customer_id}/edit', data={
        'name': '<img src=x onerror=alert(1)>',
        'city': 'Warszawa',
        'age': 30
    })

    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

    with client.application.app_context():
        unchanged_customer = Customer.query.get(customer_id)
        assert unchanged_customer.name == 'Bezpieczny Klient'

# --- SCENARIUSZ 4B: EDYCJA - XSS W POLU CITY ---
def test_edit_customer_invalid_xss_in_city(client):
    """Testuje odrzucenie próby wstrzyknięcia payloadu w polu city podczas edycji klienta."""
    with client.application.app_context():
        customer = Customer(name='Bezpieczny Klient', city='Warszawa', age=30)
        db.session.add(customer)
        db.session.commit()
        customer_id = customer.id

    response = client.post(f'/customers/{customer_id}/edit', data={
        'name': 'Bezpieczny Klient',
        'city': '<img src=x onerror=alert(1)>',
        'age': 30
    })

    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

    with client.application.app_context():
        unchanged_customer = Customer.query.get(customer_id)
        assert unchanged_customer.city == 'Warszawa'