from flask import render_template, Blueprint, request, redirect, url_for, jsonify
from project import db
from project.books.models import Book, _clean_text
from project.books.forms import CreateBook

# Blueprint for books
books = Blueprint('books', __name__, template_folder='templates', url_prefix='/books')


# Route to display books in HTML
@books.route('/', methods=['GET'])
def list_books():
    books_list = Book.query.all()
    print('Books page accessed')
    return render_template('books.html', books=books_list)


# Route to fetch books in JSON format
@books.route('/json', methods=['GET'])
def list_books_json():
    books_list = Book.query.all()
    book_list = [
        {'name': b.name, 'author': b.author, 'year_published': b.year_published, 'book_type': b.book_type}
        for b in books_list
    ]
    return jsonify(books=book_list)


# Route to create a new book
@books.route('/create', methods=['POST', 'GET'])
def create_book():
    data = request.get_json()

    try:
        # Sanityzacja i walidacja danych
        name = _clean_text(data['name'], "Book name", allow_digits=True)
        author = _clean_text(data['author'], "Author", allow_digits=False)
        book_type = _clean_text(data['book_type'], "Book type")
        year_published = int(data['year_published'])

        new_book = Book(name=name, author=author, year_published=year_published, book_type=book_type)
        db.session.add(new_book)
        db.session.commit()

        print('Book added successfully')
        return redirect(url_for('books.list_books'))

    except Exception as e:
        db.session.rollback()
        print(f'Error creating book: {e}')
        return jsonify({'error': f'Error creating book: {str(e)}'}), 400


# Route to update an existing book
@books.route('/<int:book_id>/edit', methods=['POST'])
def edit_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        print('Book not found')
        return jsonify({'error': 'Book not found'}), 404

    try:
        data = request.get_json()

        # Jeśli pola są obecne, walidujemy i sanitizujemy
        if 'name' in data:
            book.name = _clean_text(data['name'], "Book name", allow_digits=True)
        if 'author' in data:
            book.author = _clean_text(data['author'], "Author", allow_digits=False)
        if 'book_type' in data:
            book.book_type = _clean_text(data['book_type'], "Book type")
        if 'year_published' in data:
            book.year_published = int(data['year_published'])

        db.session.commit()
        print('Book edited successfully')
        return jsonify({'message': 'Book updated successfully'})

    except Exception as e:
        db.session.rollback()
        print(f'Error updating book: {e}')
        return jsonify({'error': f'Error updating book: {str(e)}'}), 400


# Route to fetch existing book data for editing
@books.route('/<int:book_id>/edit-data', methods=['GET'])
def get_book_for_edit(book_id):
    book = Book.query.get(book_id)
    if not book:
        print('Book not found')
        return jsonify({'success': False, 'error': 'Book not found'}), 404

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
        db.session.delete(book)
        db.session.commit()
        print('Book deleted successfully')
        return redirect(url_for('books.list_books'))
    except Exception as e:
        db.session.rollback()
        print(f'Error deleting book: {e}')
        return jsonify({'error': f'Error deleting book: {str(e)}'}), 500


# Route to get book details based on book name
@books.route('/details/<string:book_name>', methods=['GET'])
def get_book_details(book_name):
    book = Book.query.filter_by(name=book_name).first()
    if not book:
        print('Book not found')
        return jsonify({'error': 'Book not found'}), 404

    book_data = {
        'name': book.name,
        'author': book.author,
        'year_published': book.year_published,
        'book_type': book.book_type
    }
    return jsonify(book=book_data)
