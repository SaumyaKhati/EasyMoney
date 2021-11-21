from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10))
    category = db.Column(db.String(150))
    item = db.Column(db.String(150))
    price = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150), unique=True)
    transactions = db.relationship('Transaction')
    portfolio = db.relationship('Portfolio')

class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    monthly_income = db.Column(db.Float, default=0.0)
    savings_percent = db.Column(db.Float, default=0.0)
    subscription_total = db.Column(db.Float, default=0.0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
