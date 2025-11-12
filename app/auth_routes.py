from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user, LoginManager
from app import db
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import SignupForm, LoginForm

auth_bp = Blueprint('auth', __name__)

# -------- SIGNUP -------- #
@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()  # create form object
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered.', 'danger')
        else:
            new_user = User(username=form.username.data, email=form.email.data)
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash('Signup successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
    return render_template('signup.html', form=form)  # ← pass form to template


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()  # create form object
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Welcome back!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid credentials.', 'danger')
    return render_template('login.html', form=form)  # ← pass form to template



# -------- LOGOUT -------- #
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
