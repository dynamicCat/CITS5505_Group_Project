from flask import render_template, request, redirect, url_for, flash, session
from . import bp as profile_bp
from app.models import db, User
from flask_login import login_required, current_user


from .forms import UserProfileForm  # For profile/routes.py




import requests
def search_pexels_images(query):
    """
    Fetches images from the Pexels API based on the search query provided.
    Args:
        query (str): Search term for images.
    Returns:
        list: A list of image data if successful, otherwise an empty list.
    """
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
@login_required
def update_profile():
    """
    Route to update the current user's profile.
    On GET, display the profile form pre-filled with current user data.
    On POST, if form validation is successful, update user data in the database.
    """
    form = UserProfileForm(obj=current_user)
    if form.validate_on_submit():
        form.populate_obj(current_user)
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('profile.update_profile'))
    return render_template('profile/update_profile.html', form=form, user=current_user)

@profile_bp.route('/search_avatar', methods=['GET', 'POST'])
@login_required
def search_avatar():
    """
    Route to search for avatar images using an external API (Pexels).
    If a POST request is made with a search query, fetch images and display them.
    """
    form = UserProfileForm()  
    if request.method == 'POST' and 'submit_search' in request.form:
        images = search_pexels_images(form.image_search.data)
        if images:
            return render_template('profile/search_avatar.html', form=form, images=images, user=current_user)
        else:
            flash('No images found. Try another search.', 'error')
    return render_template('profile/search_avatar.html', form=form, user=current_user)

@profile_bp.route('/set_avatar')
@login_required
def set_avatar():

    """
    Route to set a selected image URL as the current user's avatar.
    Expects an image URL to be provided as a query parameter.
    Updates the user's avatar URL in the database and redirects to the profile update page.
    """
    image_url = request.args.get('image_url')
    if current_user:
        current_user.avatar_url = image_url
        db.session.commit()
        flash('Avatar updated successfully!', 'success')
    return redirect(url_for('profile.update_profile'))

