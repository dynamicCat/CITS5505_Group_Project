from flask import render_template, redirect, url_for, flash, session
from flask_login import login_required, current_user
from . import bp as dashboard_bp
from app.models import db,User, Request, Response


@dashboard_bp.route('/dashboard')
@login_required
def dashboard():

    """
    Serves the dashboard page to authenticated users.
    Fetches data related to the current user's requests, responses, and accepted requests.
    Redirects to login page if the user is not authenticated.
    """

    user = current_user
    if user.is_authenticated:
        user_requests = Request.query.filter_by(user_id=user.id).all()
        user_responses = Response.query.filter_by(user_id=user.id).all()
        accepted_requests = current_user.accepted_requests
        return render_template('dashboard/dashboard.html', user=user, requests=user_requests,responses=user_responses, accepted_requests=accepted_requests)
        
    return redirect(url_for('auth.login'))

