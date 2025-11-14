from flask import render_template, Blueprint, request, redirect, url_for, jsonify
from project.books.views import sanitize_field
from project import db
from project.loans.models import Loan
from project.loans.forms import CreateLoan
from project.books.models import Book
from project.customers.models import Customer
from datetime import date
from project.constants import (
    AUTHOR_NAME_RE, 
    BOOK_NAME_RE, 
    MAX_NAME_OR_AUTHOR_LENGTH, 
    MAX_BOOK_TYPE_OR_STATUS_LENGTH
)

# Blueprint for loans
loans = Blueprint('loans', __name__, template_folder='templates', url_prefix='/loans')


# Route to provide book and customer data in JSON format
@loans.route('/books/json', methods=['GET'])
def list_books_json():
    # Fetch all books from the database
    books = Book.query.all()
    # Create a list of book names
    book_list = [{'name': book.name} for book in books]
    # Return book data in JSON format
    return jsonify({'books': book_list})


# Route to list all customers
@loans.route('/customers/json', methods=['GET'])
def list_customers_json():

    # Fetch all customers from the database
    customers = Customer.query.all()
    # Create a list of customer names
    customer_list = [{'name': customer.name} for customer in customers]
    # Return customer data in JSON format
    return jsonify({'customers': customer_list})


# Route to list all loans
@loans.route('/', methods=['GET'])
def list_loans():
    # Fetch all loans from the database
    loans = Loan.query.all()
    # Render the loans.html template with the loans
    print('Loans page accessed')
    return render_template('loans.html', loans=loans, form=CreateLoan())


# Route to handle loan creation form
@loans.route('/create', methods=['POST'])
def create_loan():
    form = CreateLoan()

    if request.method == 'POST':
        
        # Process form submission
        customer_name = sanitize_field(form.customer_name.data)
        book_name = sanitize_field(form.book_name.data)
        loan_date = form.loan_date.data
        return_date = form.return_date.data

        # Check if the book is available
        book = Book.query.filter_by(name=book_name, status='available').first()
        if not book:
            print('Error. Book not available for loan.')
            return jsonify({'error': 'Book not available for loan.'}), 400

        original_author = book.author
        original_year_published = book.year_published
        original_book_type = book.book_type
        
        error = validate_loan_inputs(
            customer_name, book_name, loan_date, return_date,
            original_author, original_year_published, original_book_type
        )
        if error:
            return jsonify({"error": error}), 400
        
        try:
            # Create a new loan and store original book details
            new_loan = Loan(
                customer_name=customer_name,
                book_name=book_name,
                loan_date=loan_date,
                return_date=return_date,
                original_author=book.author,
                original_year_published=book.year_published,
                original_book_type=book.book_type
            )

            # Add the new loan to the database
            db.session.add(new_loan)
            db.session.commit()
            print('Loan added successfully')

            # Remove the book from the database
            db.session.delete(book)
            db.session.commit()

            # Redirect to the list of loans
            return redirect(url_for('loans.list_loans'))
        except Exception as e:
            db.session.rollback()
            error_message = f'Error creating loan: {str(e)}'
            # Log the error message
            print('Error creating loan:', error_message)
            return jsonify({'error': error_message}), 500

    # GET request, render the form
    print('GET request, render the form')
    return render_template('loans.html', form=form)


# Route to get loan data in JSON format
@loans.route('/json', methods=['GET'])
def list_loans_json():
    # Fetch all loans from the database
    loans = Loan.query.all()
    # Create a list of loan details
    loan_list = [{'customer_name': loan.customer_name, 'book_name': loan.book_name,
                  'loan_date': loan.loan_date, 'return_date': loan.return_date} for loan in loans]
    # Return loan data in JSON format
    return jsonify(loans=loan_list)


# Route to get customer data by name in JSON format
@loans.route('/customers/details/<string:customer_name>', methods=['GET'])
def get_customer_details(customer_name):
    # Find the customer by their name
    customer = Customer.query.filter_by(name=customer_name).first()

    if customer:
        # Create a dictionary with customer details
        customer_data = {
            'id': customer.id,
            'name': customer.name,
            'city': customer.city,
            'age': customer.age
        }
        # Return customer data in JSON format
        return jsonify(customer=customer_data)
    else:
        print('Customer not found')
        return jsonify({'error': 'Customer not found'}), 404


# Route to delete a loan
@loans.route('/<int:loan_id>/delete', methods=['POST'])
def delete_loan(loan_id):
    loan = Loan.query.get(loan_id)
    if not loan:
        print('Loan not found')
        return jsonify({'error': 'Loan not found'}), 404

    try:
        # Retrieve the book associated with the loan
        book = Book(
            name=loan.book_name,
            author=loan.original_author,
            year_published=loan.original_year_published,
            book_type=loan.original_book_type,
            status='available'  
        )

        # Add the book to the database
        db.session.add(book)

        # Delete the loan from the database
        db.session.delete(loan)
        db.session.commit()
        print('Loan deleted successfully')
        # Redirect to the list of loans
        return redirect(url_for('loans.list_loans'))
    except Exception as e:
        db.session.rollback()
        error_message = f'Error deleting loan: {str(e)}'
        print('Error deleting loan:', error_message)  # Log the error message
        return jsonify({'error': error_message}), 500


# Route to fetch loan details by ID
@loans.route('/<int:loan_id>/details', methods=['GET'])
def get_loan_details(loan_id):
    # Find the loan by ID
    loan = Loan.query.get(loan_id)

    if loan:
        # Create a dictionary with loan details
        loan_data = {
            'id': loan.id,
            'customer_name': loan.customer_name,
            'book_name': loan.book_name,
            'loan_date': loan.loan_date,
            'return_date': loan.return_date
        }
        # Return loan data in JSON format
        return jsonify(loan=loan_data)
    else:
        print('Loan not found')
        return jsonify({'error': 'Loan not found'}), 404


# Route to get book details by name in JSON format
@loans.route('/books/details/<string:book_name>', methods=['GET'])
def get_book_details(book_name):
    # Check if the book is in the "loans" database
    loaned_book = Loan.query.filter_by(book_name=book_name).first()

    if loaned_book:
        # Book is in "loans" database, return its details
        book_data = {
            'id': loaned_book.id,
            'name': loaned_book.book_name,
            'author': loaned_book.original_author,
            'year_published': loaned_book.original_year_published,
            'book_type': loaned_book.original_book_type
        }
        return jsonify(book=book_data)
    else:
        # Book not found in "loans" database, proceed to check "books" database
        book = Book.query.filter_by(name=book_name).first()

        if book:
            # Book found in "books" database, return its details
            book_data = {
                'id': book.id,
                'name': book.name,
                'author': book.author,
                'year_published': book.year_published,
                'book_type': book.book_type
            }
            return jsonify(book=book_data)
        else:
            # Book not found in both "loans" and "books" databases
            print('Book not found')
            return jsonify({'error': 'Book not found'}), 404

def validate_loan_inputs(customer_name, book_name, loan_date, return_date, original_author, original_year_published, original_book_type):
    """Waliduje dane wejściowe dla wypożyczenia, zwraca błąd lub None."""
    try:
        if len(customer_name) > MAX_NAME_OR_AUTHOR_LENGTH or not AUTHOR_NAME_RE.fullmatch(customer_name):
            return "Invalid customer name format or length."
        
        if len(book_name) > MAX_NAME_OR_AUTHOR_LENGTH or not BOOK_NAME_RE.fullmatch(book_name):
            return "Invalid book name format or length."
            
        if len(original_author) > MAX_NAME_OR_AUTHOR_LENGTH or not AUTHOR_NAME_RE.fullmatch(original_author):
            return "Invalid original author name format or length."
        
        if len(original_book_type) > MAX_BOOK_TYPE_OR_STATUS_LENGTH:
             return "Original book type too long."

        current_year = date.today().year
        if not isinstance(original_year_published, int) or original_year_published > current_year or original_year_published < 0:
            return "Original year published must be between 0 and the current year."
        
        if not isinstance(loan_date, date):
            return "Loan date must be a valid date object."
        if not isinstance(return_date, date):
            return "Return date must be a valid date object."
        
        if return_date < loan_date:
            return "Return date cannot be before the loan date."
    
    except Exception as e:
        return f"Validation error: {str(e)}"

    return None # Brak błędów