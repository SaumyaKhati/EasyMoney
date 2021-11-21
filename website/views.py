from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from website.models import Transaction
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

