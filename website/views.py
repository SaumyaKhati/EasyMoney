from flask import Blueprint, render_template, request, flash
from flask.helpers import url_for
from flask_login import login_required, current_user
from werkzeug.utils import redirect
from website.models import Transaction, Portfolio
from . import db, constant
from sqlalchemy import desc
import datetime

views = Blueprint('views', __name__)

# Defines root page. 
@views.route('/')
@login_required
def home():
    transactions = db.session.query(Transaction).filter_by(user_id=current_user.id).order_by(desc(Transaction.date))
    return render_template("home.html", user=current_user, transactions=transactions)

@views.route('/portfolio')
@login_required
def portfolio():
    query = db.session.query(Portfolio).filter_by(user_id=current_user.id).first()
    monthly_income = float(query.monthly_income)
    savings_percent = float(query.savings_percent)
    subscription_total = float(query.subscription_total)
    
    return render_template('portfolio.html', user=current_user, 
        monthly_income=monthly_income, 
        savings_percent=savings_percent,
        subscription_total=subscription_total)

@views.route('/portfolio/update', methods=['GET', 'POST'])
@login_required
def update():
    if request.method == 'POST':
        monthly_income = request.form.get('monthly_income')
        savings_percent = request.form.get('savings_percent')
        subscription_total = request.form.get('subscription_total')
        update_income = True if (monthly_income != '') else False
        update_savings = True if (savings_percent != '') else False
        update_subs = True if (subscription_total != '') else False

        # Validate input.
        try:
            monthly_income = float(monthly_income) if update_income else 0
            savings_percent = float(savings_percent) if update_savings else 0
            subscription_total = float(subscription_total) if update_subs else 0

            # Can't have negative income, costs or saving %
            if monthly_income < 0 or savings_percent < 0 or subscription_total < 0:
                flash('Please enter non-negative numeric values!', category='error')
            else:
                flash('Portfolio successfully updated!', category='success')
                # Store portfolio var.
                user_portfolio= db.session.query(Portfolio).\
                    filter_by(user_id=current_user.id)
                
                # Update relevant values.
                if update_income:
                    user_portfolio.update({'monthly_income':monthly_income})
                if update_savings:
                    user_portfolio.update({'savings_percent':savings_percent})
                if update_subs:
                    user_portfolio.update({'subscription_total':subscription_total})
                db.session.commit()
                return redirect(url_for('views.portfolio'))
            
        except:
            flash('Please enter valid numeric values for the fields!', category='error')

    return render_template('update_portfolio.html', user=current_user)


@views.route('/add', methods=['GET', 'POST'])
@login_required
def add_item():
    if request.method == 'POST':
        date = request.form.get('date')
        category = request.form.get('category')
        item = request.form.get('item')
        price = request.form.get('price')
        error = False

        # Validate Input. 
        try:
            datetime.datetime.strptime(date, "%Y-%m-%d")
        except:
            flash('Invalid date format!', category='error')
        if category == "Choose...":
            flash('You did not choose a category!', category='error')
            error = True
        if len(item) < 2:
            flash('Item name must be > 2 char.', category='error')
            error = True
        try:
            price = float(price)
            if price < 0:
                flash("You cannot enter a negative price.", category='error')
                error = True
        except ValueError:
            flash("Invalid price format. Please enter a numeric value only!", category='error')
            error = True
        
        if not error:
            flash('Transaction added!', category='success')
            entry = Transaction(date=date, category=category, item=item, price=price, user_id=current_user.id)
            db.session.add(entry)
            db.session.commit()

    return render_template('add_item.html', user=current_user, categories=constant.ACCEPTED_CATEGORIES)

