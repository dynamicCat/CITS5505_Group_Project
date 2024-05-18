from flask import render_template
from . import bp as main_bp
from flask_login import current_user

@main_bp.route('/')
def home():
    user = current_user
    if user.is_authenticated:
        return render_template('main/introductory.html', user=user)
        
    return render_template('main/introductory.html')


