from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class PostsForm(FlaskForm):
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


class LoginForm(FlaskForm):
    email = StringField('Email',
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField('Password',
        validators=[
            DataRequired()
        ]
    )

    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    f_name = StringField('First Name',
        validators=[
            DataRequired(),
            Length(min=4, max=30)
        ])
    l_name = StringField('Last Name',
        validators=[
            DataRequired(),
            Length(min=4, max=30)
        ])
    email = StringField('Email',
        validators=[
            DataRequired(),
            Email()
        ])
    submit = SubmitField('Update')
