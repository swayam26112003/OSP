from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms import *
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt


class ProductForm(FlaskForm):
    Productname = StringField(label="Product Name", validators=[InputRequired(), Length(min=1, max=100)])
    price = IntegerField(label="Price(in Rs.)", validators=[InputRequired()])
    Mfgdate =DateField(label="Manufacturing Date", validators=[InputRequired()])
    image = FileField(label='Upload an image for object',validators=[InputRequired()])
    Mfgcompany = StringField(label="Manufacturing Company", validators=[InputRequired(), Length(min=1, max=100)])
    Quantity = IntegerField(label="Quantity", validators=[InputRequired()])
    weight=FloatField(label="Weight of product" ,validators=[InputRequired()])
    Description = TextAreaField(label="Description",validators=[InputRequired(), Length(min=1, max=1000)])
    Category = StringField(label="Category", validators=[InputRequired(), Length(min=1, max=1000)])
    submit = SubmitField('Upload')
class ChangeProductForm(FlaskForm):
    Productname = StringField(label="Product Name",default=None)
    price = IntegerField(label="Price(in Rs.)",default=None )
    Mfgdate =DateField(label="Manufacturing Date",default=None)
    # image = FileField(label='Upload an image for object',default=None)
    Mfgcompany = StringField(label="Manufacturing Company", validators=[ Length(min=1, max=100)],default=None)
    Quantity = IntegerField(label="Quantity",default=None)
    weight=FloatField(label="Weight of product",default=None)
    # Description = TextAreaField(label="Description",default=None)
    Category = StringField(label="Category", validators=[Length(min=1, max=1000)],default=None)
    submit = SubmitField('Update')
