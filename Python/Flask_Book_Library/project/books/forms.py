# Form imports
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired

from project.books.models import BookChecker

checker = BookChecker()

# Flask forms (wtforms) allow you to easily create forms in format:
class CreateBook(FlaskForm):
    name = StringField('Book Name', validators=[DataRequired()])
    author = StringField('Author')
    year_published = IntegerField('Year Published', validators=[DataRequired()])
    book_type = SelectField('Book Type', choices=checker.book_types, validators=[DataRequired()])
    submit = SubmitField('Create Book')
