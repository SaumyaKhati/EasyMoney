from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = ''
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#everything above this is unchanged

class User(db.Model):

#    __tablename__ = 'feedback'
#    id = db.Column(db.Integer, primary_key=True)
#    customer = db.Column(db.String(200), unique=True)
#    dealer = db.Column(db.String(200))
#    rating = db.Column(db.Integer)
#    comments = db.Column(db.Text())

    def __init__(self, name, email, monthly_income, savings_percent):
        self.name = name
        self.email = email
        self.monthly_income = monthly_income
        self.savings_percent = savings_percent
        self.monthly_payments = [] # [["category", cost, "date"], ["category", cost, "date"]]
        self.purchases = []

    def remaining_money(self):
        total_spent = 0
        for i in self.purchases:
            total_spent += self.purchases[i][1]
        for i in self.monthly_payments:
            total_spent += self.monthly_payments[i][1]
        return self.monthly_income - self.monthly_income * self.savings_percent - total_spent

    def overspending(self):
        return self.remaining_money < 0

    from datetime import datetime #imports here temparilariy
    from calendar import monthrange
    import math

    def allowance(self):
        weekly = 0
        daily = 0
        currentMonth = datetime.now().month
        currentYear = datetime.now().year
        num_days = monthrange(currentYear, currentMonth)[1] # days left in month
        num_weeks = math.ceil(num_days/7)

        money_left = self.remaining_money()

        daily = money_left/num_days
        weekly = money_left/num_weeks

        return daily, weekly

    def expensive_categories(self):
        cat_costs = {
            "Loans/Debt": 0, 
            "Subscriptions": 0, 
            "Housing": 0, 
            "Food": 0,
            "Entertainment": 0, 
            "Misc": 0,  
        }

        for category, cost in self.monthly_payments:
            cat_costs[category] += cost
        for category, cost in self.purchases:
            cat_costs[category] += cost
        # maybe add percents too?
        return sorted(cat_costs.items(), key = lambda x: x[1])

    
