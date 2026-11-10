import os
import unittest
from datetime import datetime

os.environ['DATABASE_URL'] = 'sqlite:///:memory:'

from project import app, db
from project.books.models import Book
from project.customers.models import Customer
from project.loans.models import Loan
from project.validation import validate_text


PAYLOADS = (
    "Tytuł <script>alert('XSS w tytule')</script>",
    "Autor <script>alert('XSS w autorze')</script>",
    "Imię <script>alert('XSS w imieniu')</script>",
    "Miasto <script>alert('XSS w mieście')</script>",
    '<img src=x onerror=alert(1)>',
    '<svg/onload=alert(1)>',
    '</td><ScRiPt>alert(1)</ScRiPt>',
)
BOOK = dict(name='Solaris', author='Stanisław Lem', year_published=1961, book_type='5days')
CUSTOMER = dict(name="Anna O'Connor", city='Łódź', age=23)
LOAN = dict(customer_name=CUSTOMER['name'], book_name=BOOK['name'],
            loan_date='2026-11-10', return_date='2026-11-15')


class TextValidationTests(unittest.TestCase):
    def test_accepts_normal_text_without_changing_it(self):
        for value in ('Solaris', 'Łódź', "O'Connor", 'Żółw & przyjaciele',
                      '\u201eSolaris\u201d', 'Cafe\u0301', '  Jan Nowak  ', 'A' * 64):
            with self.subTest(value=value):
                self.assertEqual(validate_text('name', value), value)

    def test_rejects_xss_and_invalid_values(self):
        for value in PAYLOADS + ('', '   ', 'A' * 65, None, 23, [], {}, 'Jan\nNowak', 'Jan\x00'):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    validate_text('name', value)

    def test_models_validate_construction_and_assignment(self):
        loan = dict(customer_name='Anna', book_name='Solaris',
                    loan_date=datetime(2026, 11, 10), return_date=datetime(2026, 11, 15),
                    original_author='Lem', original_year_published=1961,
                    original_book_type='5days')
        for model, values, fields in (
            (Book, BOOK, ('name', 'author')),
            (Customer, CUSTOMER, ('name', 'city')),
            (Loan, loan, ('customer_name', 'book_name', 'original_author')),
        ):
            for field in fields:
                for payload in PAYLOADS:
                    with self.subTest(model=model.__name__, field=field, payload=payload):
                        with self.assertRaises(ValueError):
                            model(**dict(values, **{field: payload}))
                        item = model(**values)
                        with self.assertRaises(ValueError):
                            setattr(item, field, payload)
                        self.assertEqual(getattr(item, field), values[field])


class RequestValidationTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.context = app.app_context()
        self.context.push()
        db.create_all()
        self.client = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.context.pop()

    def add_book(self):
        self.assertEqual(self.client.post('/books/create', json=BOOK).status_code, 302)
        return Book.query.one().id

    def test_book_create_and_edit_validate_name_and_author(self):
        for field in ('name', 'author'):
            for payload in PAYLOADS:
                with self.subTest(operation='create', field=field, payload=payload):
                    data = dict(BOOK, **{field: payload})
                    response = self.client.post('/books/create', json=data)
                    self.assertEqual(response.status_code, 400)
                    self.assertIn('error', response.get_json())
                    self.assertEqual(Book.query.count(), 0)
        book_id = self.add_book()
        for field in ('name', 'author'):
            data = dict(name='Nowy tytuł', author='Nowy autor')
            data[field] = PAYLOADS[4]
            with self.subTest(operation='edit', field=field):
                response = self.client.post(f'/books/{book_id}/edit', json=data)
                self.assertEqual(response.status_code, 400)
                book = db.session.get(Book, book_id)
                self.assertEqual((book.name, book.author), ('Solaris', 'Stanisław Lem'))

    def test_customer_create_and_edit_validate_name_and_city(self):
        for field in ('name', 'city'):
            for payload in PAYLOADS:
                with self.subTest(operation='create', field=field, payload=payload):
                    data = dict(CUSTOMER, **{field: payload})
                    response = self.client.post('/customers/create', data=data)
                    self.assertEqual(response.status_code, 400)
                    self.assertEqual(Customer.query.count(), 0)
        self.assertEqual(self.client.post('/customers/create', data=CUSTOMER).status_code, 302)
        customer_id = Customer.query.one().id
        for field in ('name', 'city'):
            data = dict(name='Jan Nowak', city='Gdańsk', age=30)
            data[field] = PAYLOADS[4]
            with self.subTest(operation='edit', field=field):
                response = self.client.post(f'/customers/{customer_id}/edit', data=data)
                self.assertEqual(response.status_code, 400)
                customer = db.session.get(Customer, customer_id)
                self.assertEqual((customer.name, customer.city, customer.age),
                                 (CUSTOMER['name'], 'Łódź', 23))

    def test_loan_rejects_submitted_xss_and_unsafe_book_copies(self):
        self.add_book()
        response = self.client.post('/loans/create', data=dict(LOAN, customer_name=PAYLOADS[2]))
        self.assertEqual(response.status_code, 400)
        for field in ('name', 'author'):
            with self.subTest(field=field):
                # SQL symuluje niepoprawny wpis zapisany przed poprawką.
                db.session.execute(db.update(Book).values(**{field: PAYLOADS[4]}))
                db.session.commit()
                data = dict(LOAN)
                if field == 'name':
                    data['book_name'] = PAYLOADS[4]
                self.assertEqual(self.client.post('/loans/create', data=data).status_code, 400)
                self.assertEqual(Loan.query.count(), 0)
                self.assertEqual(Book.query.count(), 1)
                db.session.execute(db.update(Book).values(**{field: BOOK[field]}))
                db.session.commit()

    def test_valid_create_edit_loan_and_return(self):
        book_id = self.add_book()
        response = self.client.post(f'/books/{book_id}/edit', json={'author': "Lem & O'Connor"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.post('/customers/create', data=CUSTOMER).status_code, 302)
        customer_id = Customer.query.one().id
        self.assertEqual(self.client.post(f'/customers/{customer_id}/edit',
                         data=dict(CUSTOMER, city='Gdańsk')).status_code, 302)
        self.assertEqual(self.client.post('/loans/create', data=LOAN).status_code, 302)
        loan_id = Loan.query.one().id
        self.assertEqual(Book.query.count(), 0)
        self.assertEqual(self.client.post(f'/loans/{loan_id}/delete').status_code, 302)
        self.assertEqual(Loan.query.count(), 0)
        self.assertEqual(Book.query.one().author, "Lem & O'Connor")

    def test_unsafe_legacy_loan_cannot_restore_a_book(self):
        self.add_book()
        self.client.post('/loans/create', data=LOAN)
        loan_id = Loan.query.one().id
        for field in ('book_name', 'original_author'):
            with self.subTest(field=field):
                original = getattr(db.session.get(Loan, loan_id), field)
                db.session.execute(db.update(Loan).values(**{field: PAYLOADS[4]}))
                db.session.commit()
                self.assertEqual(self.client.post(f'/loans/{loan_id}/delete').status_code, 400)
                self.assertEqual(Book.query.count(), 0)
                self.assertEqual(Loan.query.count(), 1)
                db.session.execute(db.update(Loan).values(**{field: original}))
                db.session.commit()

    def test_loan_list_escapes_the_script_payloads_from_screenshots(self):
        self.add_book()
        self.client.post('/customers/create', data=CUSTOMER)
        self.client.post('/loans/create', data=LOAN)
        # Rekord sprzed poprawki zawiera skrypty skopiowane do wypożyczenia.
        db.session.execute(db.update(Loan).values(
            customer_name=PAYLOADS[2], book_name=PAYLOADS[0]))
        db.session.commit()

        response = self.client.get('/loans/')
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertNotIn(PAYLOADS[2], html)
        self.assertNotIn(PAYLOADS[0], html)
        self.assertIn('Imię &lt;script&gt;', html)
        self.assertIn('Tytuł &lt;script&gt;', html)
        loan = Loan.query.one()
        self.assertEqual(loan.customer_name, PAYLOADS[2])
        self.assertEqual(loan.book_name, PAYLOADS[0])

    def test_old_xss_is_escaped_on_all_lists(self):
        self.add_book()
        self.client.post('/customers/create', data=CUSTOMER)
        self.client.post('/loans/create', data=LOAN)
        db.session.execute(db.insert(Book).values(**BOOK))
        db.session.execute(db.update(Book).values(name=PAYLOADS[4], author=PAYLOADS[4]))
        db.session.execute(db.update(Customer).values(name=PAYLOADS[4], city=PAYLOADS[4]))
        db.session.execute(db.update(Loan).values(customer_name=PAYLOADS[4], book_name=PAYLOADS[4]))
        db.session.commit()
        for path in ('/books/', '/customers/', '/loans/'):
            with self.subTest(path=path):
                html = self.client.get(path).get_data(as_text=True)
                self.assertNotIn(PAYLOADS[4], html)
                self.assertIn('&lt;img', html)


if __name__ == '__main__':
    unittest.main()
