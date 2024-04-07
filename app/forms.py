# Add any form classes for Flask-WTF here
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length, ValidationError
from werkzeug.utils import secure_filename
import os

# Custom validator to check if the uploaded file is an image
def is_image(form, field):
    if field.data:
        filename = secure_filename(field.data.filename)
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            raise ValidationError('Only image files are allowed.')

class MovieForm(FlaskForm):
    title = StringField('Movie Title', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    poster = FileField('Movie Poster', validators=[DataRequired(), is_image])