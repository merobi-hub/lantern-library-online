from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email
from flask_login import UserMixin

class UserLoginForm(FlaskForm,UserMixin):
    #username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit_button = SubmitField()

class BlogPostForm(FlaskForm):
    title = TextAreaField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', render_kw={"rows": 20, "cols": 50}, validators=[DataRequired()])
    submit_button = SubmitField()

class AddBookForm(FlaskForm):
    author = TextAreaField('Author', validators=[DataRequired()])
    title = TextAreaField('Title', validators=[DataRequired()])
    submit_button = SubmitField()

class UpdateBookForm(FlaskForm):
    author = TextAreaField('Author', validators=[DataRequired()])
    title = TextAreaField('Title', validators=[DataRequired()])
    publisher = TextAreaField('Publisher')
    description = TextAreaField('Description')
    genre = TextAreaField('Genre')
    pub_date = TextAreaField('Publication Date')
    submit_button = SubmitField()
    