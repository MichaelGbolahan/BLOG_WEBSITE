from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed
from .models import User




class RegisterUser(FlaskForm):
    name=StringField('Name',validators=[DataRequired()])
    username=StringField('Username',validators=[DataRequired()])
    email = StringField('Email:', validators=[Email(), DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match!')])
    confirm = PasswordField('Repeat password:', validators=[DataRequired()])
    profile = FileField('Profile Image', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Image only please!')])
    submit=SubmitField('submit')

    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('username is already taken. please choose a different one.')

    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('email is already registered. please choose a different one.')



class LoginUser(FlaskForm):
    username=StringField('Username',validators=[DataRequired()])
    password=PasswordField('Password',validators=[DataRequired()])
    submit=SubmitField('submit')