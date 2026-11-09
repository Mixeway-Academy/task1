import pytest

from project import db
from project.books.models import Book
from xss_payloads import XSS_PAYLOADS


def book_json(**overrides):
    data = {
        "name": "Poprawna książka",
        "author": "Jan Kowalski",
        "year_published": "2020",
        "book_type": "2days",
    }
    data.update(overrides)
    return data


def seed_book(app, **overrides):
    with app.app_context():
        book = Book(**book_json(**overrides))
        db.session.add(book)
        db.session.commit()
        return book.id


def books_page(client):
    response = client.get("/books/")
    assert response.status_code == 200
    return response.get_data(as_text=True)


@pytest.mark.parametrize("field", ["name", "author"])
@pytest.mark.parametrize("payload", XSS_PAYLOADS)
def test_create_rejects_xss(client, app, field, payload):
    response = client.post("/books/create", json=book_json(**{field: payload}))

    assert response.status_code == 400
    with app.app_context():
        assert Book.query.count() == 0


@pytest.mark.parametrize("field", ["name", "author"])
@pytest.mark.parametrize("payload", XSS_PAYLOADS)
def test_create_does_not_render_xss(client, field, payload):
    client.post("/books/create", json=book_json(**{field: payload}))

    assert payload not in books_page(client)


@pytest.mark.parametrize("field", ["name", "author"])
@pytest.mark.parametrize("payload", XSS_PAYLOADS)
def test_edit_does_not_render_xss(client, app, field, payload):
    book_id = seed_book(app)

    client.post(f"/books/{book_id}/edit", json={field: payload})

    assert payload not in books_page(client)


@pytest.mark.parametrize("field", ["name", "author"])
@pytest.mark.parametrize("payload", XSS_PAYLOADS)
def test_page_escapes_xss_already_in_database(client, app, field, payload):
    seed_book(app, **{field: payload})

    assert payload not in books_page(client)
