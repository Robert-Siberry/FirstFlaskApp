from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class PostsForm(FlaskForm):
    f_name = StringField(
        'First Name',
        validators=[
            DataRequired(),
            Length(min=1, max=30)
        ]
    )

    l_name = StringField(
        'Last Name',
        validators=[
            DataRequired(),
            Length(min=1, max=30)
        ]
    )

    title = StringField(
        'Title',
        validators=[
            DataRequired(),
            Length(min=4, max=100)
        ]
    )

    content = StringField(
        'Content',
        validators=[
            DataRequired(),
            Length(min=4, max=300)
        ]
    )

    submit = SubmitField('Submit a Post')


class RegistrationForm(FlaskForm):
    email = StringField('Email',
        validators = [
            DataRequired(),
            Email()
        ]
    )
    password = PasswordField('Password',
        validators = [
            DataRequired(),
        ]
    )
    confirm_password = PasswordField('Confirm Password',
        validators = [
            DataRequired(),
            EqualTo('password')
        ]
    )
    submit = SubmitField('Sign Up')