# Form imports
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length
from project.constants import MAX_NAME_OR_AUTHOR_LENGTH, MAX_CITY_LENGTH


# Flask forms (wtforms) allow you to easily create forms in this format:
class CreateCustomer(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=MAX_NAME_OR_AUTHOR_LENGTH)])  
    city = StringField('City', validators=[DataRequired(), Length(max=MAX_CITY_LENGTH)])
    age = IntegerField('Age', validators=[DataRequired()])
    submit = SubmitField('Create Customer')
