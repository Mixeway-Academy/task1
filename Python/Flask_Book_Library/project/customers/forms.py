# Form imports
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length


# Flask forms (wtforms) allow you to easily create forms in this format:
class CreateCustomer(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=64)])  
    city = StringField('City', validators=[DataRequired(), Length(max=64)])
    age = IntegerField('Age', validators=[DataRequired()])
    submit = SubmitField('Create Customer')
