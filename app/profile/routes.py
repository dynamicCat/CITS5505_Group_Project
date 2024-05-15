from flask import render_template, request, redirect, url_for, flash, session
from . import bp as profile_bp
from app.models import db, User



from .forms import UserProfileForm  # For profile/routes.py




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
    



@profile_bp.route('/update_profile', methods=['GET', 'POST'])
def update_profile():
    form = UserProfileForm()
    user = User.query.get_or_404(session['user_id'])

    if form.validate_on_submit() and 'submit_update' in request.form:
        user.username = form.username.data
        user.email = form.email.data
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('profile.update_profile'))

    return render_template('profile/update_profile.html', form=form, user=user)

@profile_bp.route('/search_avatar', methods=['GET', 'POST'])
def search_avatar():
    form = UserProfileForm()  # May need to modify or use a different form to accommodate image-only searches
    user = User.query.get_or_404(session['user_id'])

    if request.method == 'POST' and 'submit_search' in request.form:
        images = search_pexels_images(form.image_search.data)
        if images:
            return render_template('profile/search_avatar.html', form=form, images=images, user=user)
        else:
            flash('No images found. Try another search.', 'error')

    return render_template('profile/search_avatar.html', form=form, user=user)



@profile_bp.route('/set_avatar')

def set_avatar():
    image_url = request.args.get('image_url')
    user_id = session['user_id']
    user = User.query.get(user_id)
    if user:
        user.avatar_url = image_url
        db.session.commit()
        flash('Avatar updated successfully!', 'success')
    return redirect(url_for('dashboard.dashboard'))

