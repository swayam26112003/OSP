import sys
sys.path.append("...")
from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms import *
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from OSP import db


class Cart(db.Model, UserMixin):
    cartid=db.Column(db.Integer,primary_key=True)
    pid = db.Column(db.Integer)
    userid = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    
    def get_id(self):
        return (self.cartid)