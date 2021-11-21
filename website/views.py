from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from . import db
import datetime

views = Blueprint('views', __name__)

# Defines root page. 
@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/add', methods=['GET', 'POST'])
@login_required
def add_item():
    if request.method == 'POST':
        date = request.form.get('date')
        category = request.form.get('category')
        item = request.form.get('item')
        price = request.form.get('price')
    # Validate the date. 
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
    except:
        flash('Invalid date format!', category='error')

    return render_template('add_item.html', user=current_user)

