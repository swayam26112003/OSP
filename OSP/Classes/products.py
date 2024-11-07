from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms import *
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from OSP import db
class Products(db.Model, UserMixin):
    Pid = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), nullable=False)
    Sellerid = db.Column(db.Integer, primary_key=False)
    Price = db.Column(db.Integer, primary_key=False)
    Image_url = db.Column(db.String(200), nullable=False)
    mfgdate = db.Column(db.String(50), nullable=False)
    mfgcompany = db.Column(db.String(50), nullable=False)
    sellercity = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, primary_key=False)
    weight = db.Column(db.Float, primary_key=False)
    status = db.Column(db.Boolean, default=True)
    Category=db.Column(db.String(20))
    Description=db.Column(db.String(1000),nullable=True)
    def get_id(self):
        return (self.Pid)