from flask import render_template
from . import bp as main_bp
from flask_login import current_user

@main_bp.route('/')
def home():
    """
    Serves the home page of the website.
    
    Depending on the authentication status of the user, different content might be shown.
    If the user is authenticated, they are passed to the template to allow for a personalized user experience.
    
    Returns:
        render_template: The introductory page with or without user context.
    """
    user = current_user
    if user.is_authenticated:
        return render_template('main/introductory.html', user=user)
        
    return render_template('main/introductory.html')


