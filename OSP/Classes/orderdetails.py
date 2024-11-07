from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms import *
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from OSP import db


class Orderdetails(db.Model, UserMixin):
    oid = db.Column(db.Integer, primary_key=True)

    pid = db.Column(db.Integer, primary_key=False)
    cid = db.Column(db.Integer, primary_key=False)

    date = db.Column(db.String(50), nullable=False)

    quantity = db.Column(db.Integer, primary_key=False)
    Status = db.Column(db.Boolean, default=False)
    Price = db.Column(db.Integer, default=-1)

    def get_id(self):
        return (self.oid)

class OPtobepassed():
    def __init__(self,OID,name,SID,email,price,quantity,delivery):
        self.OID=OID
        self.name=name
        self.SID=SID
        self.email=email
        self.price=price
        self.quantity=quantity
        self.delivery=delivery