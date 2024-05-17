from flask import render_template, redirect, url_for, flash, session
from flask_login import login_required, current_user
from . import bp as dashboard_bp
from app.models import db,User, Request, Response

import requests
def search_pexels_images(query):
    api_key = "SwtLixI0IQ8GuhDNDwVheitnQpSbEf2kXc4sL5Mc3tl6cJ5NM7eBaIm4"
    url = "https://api.pexels.com/v1/search"
    headers = {"Authorization": api_key}
    params = {"query": query, "per_page": 10}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json().get('photos', [])  #Get 'photos' safely, or return an empty list if not found
    else:
        print(f"Failed to get photos: {response.status_code}")
        return []  # If the request fails, an empty list is returned.
@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    user = current_user
    if user.is_authenticated:
        user_requests = Request.query.filter_by(user_id=user.id).all()
        user_responses = Response.query.filter_by(user_id=user.id).all()
        accepted_requests = current_user.accepted_requests
        return render_template('dashboard/dashboard.html', user=user, requests=user_requests,responses=user_responses, accepted_requests=accepted_requests)
        
    return redirect(url_for('auth.login'))

