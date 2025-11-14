# Form imports
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length
from project.constants import MAX_NAME_OR_AUTHOR_LENGTH, MAX_BOOK_TYPE_OR_STATUS_LENGTH


# Flask forms (wtforms) allow you to easily create forms in format:
class CreateBook(FlaskForm):
    name = StringField('Book Name', validators=[DataRequired(), Length(max=MAX_NAME_OR_AUTHOR_LENGTH)])
    author = StringField('Author', validators=[Length(max=MAX_NAME_OR_AUTHOR_LENGTH)])
    year_published = IntegerField('Year Published', validators=[DataRequired()])
    book_type = SelectField('Book Type', choices=[('2days', 'Up to 2 days'), ('5days', 'Up to 5 days'), ('10days', 'Up to 10 days')], validators=[DataRequired(), Length(max=MAX_BOOK_TYPE_OR_STATUS_LENGTH)])
    submit = SubmitField('Create Book')
