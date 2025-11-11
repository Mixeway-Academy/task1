from flask import render_template, Blueprint, request, redirect, url_for, jsonify, flash
from project import db
from project.books.models import Book
from project.books.forms import CreateBook
import re

# Blueprint for books
books = Blueprint('books', __name__, template_folder='templates', url_prefix='/books')


# Route to display books in HTML
@books.route('/', methods=['GET'])
def list_books():
    # Fetch all books from the database
    books = Book.query.all()
    print('Books page accessed')
    return render_template('books.html', books=books)


# Route to fetch books in JSON format
@books.route('/json', methods=['GET'])
def list_books_json():
    # Fetch all books from the database and convert to JSON
    books = Book.query.all()
    # Create a list of dictionaries representing each book with the required fields
    book_list = [{'name': book.name, 'author': book.author, 'year_published': book.year_published, 'book_type': book.book_type} for book in books]
    return jsonify(books=book_list)


# Route to create a new book
@books.route('/create', methods=['POST', 'GET'])
def create_book():
    data = request.get_json()

    sanitized_name = data.get('name', '').strip()
    sanitized_author = data.get('author', '').strip()
    allowed_pattern = r"^[A-Za-z0-9\s\-\':,\.!]+$"

    # DB Allows max 64 characters for these fields, let's limit that. We also get rid of |safe to prevent rendering malicious HTML.
    # We don't trust the data from user input fields, thus we sanitize it first nevertheless.
    if not re.match(allowed_pattern, sanitized_name) or len(sanitized_name) > 64:
        print('Invalid book name')
        return jsonify({'error': f'Invalid book name'}), 400    # Additional verification for the length and data sanitization, but removing |safe from HTML is enough in this case.

    if not re.match(allowed_pattern, sanitized_author) or len(sanitized_author) > 64:
        print('Invalid author name')
        return jsonify({'error': f'Invalid author name'}), 400

    new_book = Book(name=sanitized_name, author=sanitized_author, year_published=data['year_published'], book_type=data['book_type'])
    
    try:
        # Add the new book to the session and commit to save to the database
        db.session.add(new_book)
        db.session.commit()
        print('Book added successfully')
        return redirect(url_for('books.list_books'))
    except Exception as e:
        # Handle any exceptions, such as database errors
        db.session.rollback()
        print('Error creating book')
        return jsonify({'error': f'Error creating book: {str(e)}'}), 500


# Route to update an existing book
@books.route('/<int:book_id>/edit', methods=['POST'])
def edit_book(book_id):
    # Get the book with the given ID
    book = Book.query.get(book_id)
    
    # Check if the book exists
    if not book:
        print('Book not found')
        return jsonify({'error': 'Book not found'}), 404

    try:
        # Get data from the request as JSON
        data = request.get_json()
        
        # Update book details
        book.name = data.get('name', book.name)  # Update if data exists, otherwise keep the same
        book.author = data.get('author', book.author)
        book.year_published = data.get('year_published', book.year_published)
        book.book_type = data.get('book_type', book.book_type)
        
        # Commit the changes to the database
        db.session.commit()
        print('Book edited successfully')
        return jsonify({'message': 'Book updated successfully'})
    except Exception as e:
        # Handle any exceptions
        db.session.rollback()
        print('Error updating book')
        return jsonify({'error': f'Error updating book: {str(e)}'}), 500


# Route to fetch existing book data for editing
@books.route('/<int:book_id>/edit-data', methods=['GET'])
def get_book_for_edit(book_id):
    # Get the book with the given ID
    book = Book.query.get(book_id)
    
    # Check if the book exists
    if not book:
        print('Book not found')
        return jsonify({'success': False, 'error': 'Book not found'}), 404

    # Create a dictionary representing the book data
    book_data = {
        'name': book.name,
        'author': book.author,
        'year_published': book.year_published,
        'book_type': book.book_type
    }
    
    return jsonify({'success': True, 'book': book_data})


# Route to delete a book
@books.route('/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        print('Book not found')
        return jsonify({'error': 'Book not found'}), 404

    try:
        # Delete the book from the database
        db.session.delete(book)
        db.session.commit()
        print('Book deleted successfully')
        return redirect(url_for('books.list_books'))
    except Exception as e:
        # Handle any exceptions, such as database errors
        db.session.rollback()
        print('Error deleting book')
        return jsonify({'error': f'Error deleting book: {str(e)}'}), 500


# Route to get book details based on book name
@books.route('/details/<string:book_name>', methods=['GET'])
def get_book_details(book_name):
        # Find the book by its name
        book = Book.query.filter_by(name=book_name).first()

        if book:
            book_data = {
                'name': book.name,
                'author': book.author,
                'year_published': book.year_published,
                'book_type': book.book_type
            }
            return jsonify(book=book_data)
        else:
            print('Book not found')
            return jsonify({'error': 'Book not found'}), 404