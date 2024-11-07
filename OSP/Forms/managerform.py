from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms import *
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from OSP import app
class MyForm(Form):
    STRING_CHOICES = [
        ('Hyderabad', 'Hyderabad'),
        ('Delhi', 'Delhi'),
        ('Kolkata', 'Kolkata'),
        ('Mumbai','Mumbai'),
        ('Chennai','Chennai')
    ]
    
class MyForm1(Form):
    STRING_CHOICES = [
        ('Telangana', 'Telangana'),
        ('Delhi', 'Delhi'),
        ('West Bengal', 'West Bengal'),
        ('Maharashtra','Maharashtra'),
        ('Tamil Nadu','Tamil Nadu')
    ]

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'loginmanager'

class RegisterManagerForm(FlaskForm):
    managername = StringField(label="Name", validators=[
        InputRequired(), Length(min=3, max=50)])
    email = EmailField(label="Email", validators=[
        InputRequired(), Length(min=11, max=50)])

    password = PasswordField(label="Password", validators=[
                             InputRequired(), Length(min=8, max=20)])
    re_password = PasswordField(label="Retype-Password", validators=[
        InputRequired(), Length(min=8, max=20)])
    phone_no = StringField(label="Phone Number", validators=[
        InputRequired(), Length(min=1, max=100)])
    street = StringField(label="Street", validators=[
        InputRequired(), Length(min=1, max=100)])
    city=SelectField(choices=MyForm.STRING_CHOICES)
    state=SelectField(choices=MyForm1.STRING_CHOICES)
    pin = StringField(label="PIN Code", validators=[
        InputRequired(), Length(min=6, max=100)])
    Gender = StringField(label="Gender", validators=[
        InputRequired()])
    dob = DateField(label="Date of Birth", validators=[
        InputRequired()])

    submit = SubmitField('Register')



        # if password.data!=re_password.data:
        #     raise ValidationError(
        #         'Passwords do not match'
        #     )


class LoginManagerForm(FlaskForm):
    email = StringField(label="Email", validators=[
        InputRequired(), Length(min=11, max=50)])

    password = PasswordField(label="Password", validators=[
                             InputRequired(), Length(min=8, max=20)])

    submit = SubmitField('Login')
