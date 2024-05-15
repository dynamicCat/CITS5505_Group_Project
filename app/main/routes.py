from flask import render_template
from . import bp as main_bp

@main_bp.route('/')
def home():
    return render_template('main/introductory.html')
