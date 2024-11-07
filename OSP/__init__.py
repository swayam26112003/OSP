import sys
sys.path.append("...")
from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/osp_db'
app.config['SECRET_KEY'] = 'thisisasecretkey'
db = SQLAlchemy(app)
