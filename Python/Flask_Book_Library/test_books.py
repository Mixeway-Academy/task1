import pytest
from project import app, db
from project.books.models import Book


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        db.create_all()

        yield app.test_client()

        db.session.remove()
        db.drop_all()


def test_create_book_success(client):
    data = {
        'name': 'Harry Potter',
        'author': 'J.K. Rowling',
        'year_published': 1997,
        'book_type': 'Fantasy'
    }

    response = client.post('/books/create', json=data)

    assert response.status_code == 302

    book = Book.query.filter_by(name='Harry Potter').first()
    assert book is not None


def test_create_book_xss_attack(client):
    data = {
        'name': '<script>alert(1)</script>',
        'author': 'Attacker',
        'year_published': 2024,
        'book_type': 'Fantasy'
    }

    response = client.post('/books/create', json=data)

    assert response.status_code == 400

    assert response.json['error'] == \
        'Invalid input detected in field: name'

    book = Book.query.filter_by(
        name='<script>alert(1)</script>'
    ).first()

    assert book is None


def test_create_book_missing_field(client):
    data = {
        'name': 'Harry Potter',
        'author': 'J.K. Rowling',
        'year_published': 1997
    }

    response = client.post('/books/create', json=data)

    assert response.status_code == 400
    assert response.json['error'] == 'Missing field: book_type'
