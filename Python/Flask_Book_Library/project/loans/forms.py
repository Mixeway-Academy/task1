# Form imports
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.fields import DateField
from wtforms.validators import DataRequired, Length
from project.constants import (
    AUTHOR_NAME_RE, 
    BOOK_NAME_RE, 
    MAX_NAME_OR_AUTHOR_LENGTH, 
    MAX_BOOK_TYPE_OR_STATUS_LENGTH
)

# Flask forms (wtforms) allow you to easily create forms in format:
class CreateLoan(FlaskForm):
    customer_name = StringField('Customer Name', validators=[DataRequired(), Length(max=MAX_NAME_OR_AUTHOR_LENGTH)])
    book_name = StringField('Book Name', validators=[DataRequired(), Length(max=MAX_NAME_OR_AUTHOR_LENGTH)])
    loan_date = DateField('Loan Date', format='%Y-%m-%d', validators=[DataRequired()])
    return_date = DateField('Return Date', format='%Y-%m-%d', validators=[DataRequired()])

    # Fields for capturing original book details
    original_author = StringField('Original Author', validators=[DataRequired(), Length(max=MAX_NAME_OR_AUTHOR_LENGTH)])
    original_year_published = IntegerField('Original Year Published', validators=[DataRequired()])
    original_book_type = StringField('Original Book Type', validators=[DataRequired(), Length(max=MAX_BOOK_TYPE_OR_STATUS_LENGTH)])

    submit = SubmitField('Create Loan')

