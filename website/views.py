from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

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

        
    return render_template('add_item.html', user=current_user)

