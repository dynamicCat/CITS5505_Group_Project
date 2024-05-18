# auth/routes.py
from flask import  render_template, redirect, url_for, flash, request, session, jsonify
from . import bp as auth_bp
from app.models import User
from .forms import LoginForm, RegistrationForm
from app import db
from flask_login import login_user, logout_user, current_user

# Authentication blueprint routes for Flask application.

@auth_bp.route('/check_username')
def check_username():
    username = request.args.get('username')
    user = User.query.filter_by(username=username).first()
    return jsonify({'available': user is None})

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Route to handle user login.
    Displays login form and handles its submission.
    If form is submitted and valid, checks if user exists and password is correct.
    If credentials are valid, logs the user in and redirects to the dashboard.
    Otherwise, displays an error message.
    """
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)  # Log in the user
            return redirect(url_for('dashboard.dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Route to handle user registration.
    Displays registration form and handles its submission.
    If form is submitted and valid, creates a new user, saves it to the database,
    and redirects to the login page.
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        user.avatar_url = '/static/images/default_avatar.jpg'
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@auth_bp.route('/logout')
def logout():
    """
    Route to handle user logout.
    Logs out the current user and redirects to the login page with a logout message.
    """
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('auth.login'))
