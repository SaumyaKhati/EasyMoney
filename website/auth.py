from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Portfolio
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import re

auth = Blueprint('auth', __name__)
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash('Logged in Successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else: 
                flash('Incorrect password, try again.', category='error')   
        else:
            flash('Email does not exist', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')  
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()

        # Basic validity check of input. 
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 3:
            flash('Email must be >= 3 characters', category='error')
        elif not re.fullmatch(regex, email):
            flash('Email is not valid.', category='error')
        elif len(username) < 2:
            flash('Username must be  >= 2 char', category='error')
        elif password1 != password2:
            flash("Passwords don't match", category='error')
        elif len(password1) < 8:
            flash('Password must be at least 8 char', category='error')
        else:
            # Add user + user's default portfolio to database.
            new_user = User(email=email, username=username, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            id = db.session.query(User).filter_by(email=email).first().id
            new_portfolio = Portfolio(monthly_income=0.0, savings_percent=0.0, subscription_total=0.0, user_id=id)
            db.session.add(new_portfolio)
            db.session.commit() # Update database.

            login_user(new_user, remember=True)
            flash('Account created!', category='success') 
            return redirect(url_for('views.home'))
    return render_template("register.html", user=current_user)