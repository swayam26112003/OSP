from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms import *
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from OSP import db

class User(db.Model, UserMixin):
    User_id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(50), nullable=False)
    Password = db.Column(db.String(50), nullable=False)
    Phone_num = db.Column(db.String(15), nullable=False)
    Street = db.Column(db.String(100), nullable=False)
    City = db.Column(db.String(100), nullable=False)
    State = db.Column(db.String(100), nullable=False)
    PIN = db.Column(db.Integer(), nullable=False)
    IsBuyer = db.Column(db.Boolean, default=True)
    IsSeller = db.Column(db.Boolean, default=True)
    balance=db.Column(db.Integer,default=0)

    def get_id(self):
        return (self.User_id)