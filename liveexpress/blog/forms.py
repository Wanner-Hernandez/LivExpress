from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import TextAreaField,StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class PostForm(FlaskForm):
    title = StringField('Post Title', validators=[DataRequired()])
    image = FileField("Choose Post image")
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

class SearchForm(FlaskForm):
    title = StringField('Search By title')
    hashtags = StringField("Search By hashtags")
    submit = SubmitField('search')

