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


class Negotiations(db.Model, UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    Pid=db.Column(db.Integer)
    seller_id = db.Column(db.Integer)
    buyer_id = db.Column(db.Integer)
    Message = db.Column(db.String(1000), nullable=False)
    price = db.Column(db.Integer)
    sender_id = db.Column(db.Integer)
    ismanager = db.Column(db.Integer,default=0)
    
    def get_id(self):
        return (self.id)