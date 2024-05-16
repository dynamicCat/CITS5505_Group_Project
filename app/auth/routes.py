# auth/routes.py
from flask import  render_template, redirect, url_for, flash, request, session
from . import bp as auth_bp
from app.models import User
from .forms import LoginForm, RegistrationForm
from app import db
#from flask_login import current_user



@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    #if current_user.is_authenticated:
    #    return redirect(url_for('dashboard.dashboard'))
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            session['user_id'] = user.id
            session['username'] = user.username
            session['avatar_url'] = user.avatar_url
            return redirect(url_for('dashboard.dashboard'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('auth/login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.')
    return redirect(url_for('auth.login'))