import pytest

from project import db
from project.customers.models import Customer
from xss_payloads import XSS_PAYLOADS


def customer_form(**overrides):
    data = {"name": "Jan Kowalski", "city": "Warszawa", "age": "30"}
    data.update(overrides)
    return data


def seed_customer(app, **overrides):
    with app.app_context():
        customer = Customer(**customer_form(**overrides))
        db.session.add(customer)
        db.session.commit()
        return customer.id


def customers_page(client):
    response = client.get("/customers/")
    assert response.status_code == 200
    return response.get_data(as_text=True)


@pytest.mark.parametrize("field", ["name", "city"])
@pytest.mark.parametrize("payload", XSS_PAYLOADS)
def test_create_rejects_xss(client, app, field, payload):
    response = client.post("/customers/create", data=customer_form(**{field: payload}))

    assert response.status_code == 400
    with app.app_context():
        assert Customer.query.count() == 0


@pytest.mark.parametrize("field", ["name", "city"])
@pytest.mark.parametrize("payload", XSS_PAYLOADS)
def test_create_does_not_render_xss(client, field, payload):
    client.post("/customers/create", data=customer_form(**{field: payload}))

    assert payload not in customers_page(client)


@pytest.mark.parametrize("field", ["name", "city"])
@pytest.mark.parametrize("payload", XSS_PAYLOADS)
def test_edit_does_not_render_xss(client, app, field, payload):
    customer_id = seed_customer(app)

    client.post(
        f"/customers/{customer_id}/edit", data=customer_form(**{field: payload})
    )

    assert payload not in customers_page(client)


@pytest.mark.parametrize("field", ["name", "city"])
@pytest.mark.parametrize("payload", XSS_PAYLOADS)
def test_page_escapes_xss_already_in_database(client, app, field, payload):
    seed_customer(app, **{field: payload})

    assert payload not in customers_page(client)
