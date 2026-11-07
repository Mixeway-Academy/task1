import pytest
from project import db
from project import app as flask_app
from project.books.models import Book

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
def test_create_book_valid_input(client):
    """Testuje poprawne dodanie książki bez niedozwolonych tagów HTML."""
    response = client.post('/books/create', json={
        'name': 'W pustyni i w puszczy',
        'author': 'Henryk Sienkiewicz',
        'year_published': 1911,
        'book_type': 'Powieść przygodowa'
    })
    
    assert response.status_code in [200, 302]
    book = Book.query.filter_by(name='W pustyni i w puszczy').first()
    assert book is not None
    assert book.author == 'Henryk Sienkiewicz'

# --- SCENARIUSZ 2A: TWORZENIE - XSS W POLU NAME ---
def test_create_book_invalid_xss_in_name(client):
    """Testuje odrzucenie payloadu w polu name przy tworzeniu."""
    response = client.post('/books/create', json={
        'name': '<img src=x onerror=alert(1)>',
        'author': 'Henryk Sienkiewicz',
        'year_published': 1911,
        'book_type': 'Powieść przygodowa'
    })
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert Book.query.count() == 0

# --- SCENARIUSZ 2B: TWORZENIE - XSS W POLU AUTHOR ---
def test_create_book_invalid_xss_in_author(client):
    """Testuje odrzucenie payloadu w polu author przy tworzeniu."""
    response = client.post('/books/create', json={
        'name': 'W pustyni i w puszczy',
        'author': '<img src=x onerror=alert(1)>',
        'year_published': 1911,
        'book_type': 'Powieść przygodowa'
    })
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert Book.query.count() == 0

# --- SCENARIUSZ 3: EDYCJA - WARIANT POPRAWNY ---
def test_edit_book_valid_input(client):
    """Testuje poprawną edycję istniejącej książki bezpiecznymi danymi."""
    with client.application.app_context():
        book = Book(name='Stara nazwa', author='Stary Autor', year_published=2000, book_type='Test')
        db.session.add(book)
        db.session.commit()
        book_id = book.id

    response = client.post(f'/books/{book_id}/edit', json={
        'name': 'Nowa nazwa książki',
        'author': 'Nowy Autor'
    })

    assert response.status_code == 200
    data = response.get_json()
    assert data.get('message') == 'Book updated successfully'

    with client.application.app_context():
        updated_book = Book.query.get(book_id)
        assert updated_book.name == 'Nowa nazwa książki'
        assert updated_book.author == 'Nowy Autor'

# --- SCENARIUSZ 4A: EDYCJA - XSS W POLU NAME ---
def test_edit_book_invalid_xss_in_name(client):
    """Testuje odrzucenie próby wstrzyknięcia payloadu w polu name podczas edycji."""
    with client.application.app_context():
        book = Book(name='Bezpieczna książka', author='Bezpieczny Autor', year_published=2020, book_type='Test')
        db.session.add(book)
        db.session.commit()
        book_id = book.id

    response = client.post(f'/books/{book_id}/edit', json={
        'name': '<img src=x onerror=alert(1)>',
        'author': 'Bezpieczny Autor'
    })

    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

    with client.application.app_context():
        unchanged_book = Book.query.get(book_id)
        assert unchanged_book.name == 'Bezpieczna książka'

# --- SCENARIUSZ 4B: EDYCJA - XSS W POLU AUTHOR ---
def test_edit_book_invalid_xss_in_author(client):
    """Testuje odrzucenie próby wstrzyknięcia payloadu w polu author podczas edycji."""
    with client.application.app_context():
        book = Book(name='Bezpieczna książka', author='Bezpieczny Autor', year_published=2020, book_type='Test')
        db.session.add(book)
        db.session.commit()
        book_id = book.id

    response = client.post(f'/books/{book_id}/edit', json={
        'name': 'Bezpieczna książka',
        'author': '<img src=x onerror=alert(1)>'
    })

    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

    with client.application.app_context():
        unchanged_book = Book.query.get(book_id)
        assert unchanged_book.author == 'Bezpieczny Autor'