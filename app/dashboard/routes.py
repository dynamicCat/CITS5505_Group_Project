from flask import render_template, redirect, url_for, flash, session

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
def dashboard():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        if user:
            user_requests = Request.query.filter_by(user_id=user_id).all()
            user_responses = Response.query.filter_by(user_id=user_id).all()
            return render_template('dashboard/dashboard.html', user=user, requests=user_requests, responses=user_responses)
        else:
            flash('User not found')
            return redirect(url_for('auth.login'))  # Assuming 'auth.login' is the correct endpoint
    else:
        flash('Please login first')
        return redirect(url_for('auth.login'))  # Assuming 'auth.login' is the correct endpoint

