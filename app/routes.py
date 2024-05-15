from flask import render_template, request, redirect, url_for, flash, session
from . import app, db
from .forms import LoginForm, RegistrationForm,UserProfileForm
from .models import User, Request, Response


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








# Routes
@app.route('/')
def home():
    return render_template('introductory.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            session['user_id'] = user.id
            session['username'] = user.username
            session['avatar_url'] = user.avatar_url
            return redirect(url_for('dashboard'))
        elif user:
            flash('Incorrect password.', 'error')
        else:
            flash('User not found.', 'error')
    return render_template('login.html', form=form)





@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username already taken. Please choose another one.', 'error')
        else:
            new_user = User(username=form.username.data)
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful. Please login.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        if user:
            user_requests = Request.query.filter_by(user_id=user_id).all()
            user_responses = Response.query.filter_by(user_id=user_id).all()
            accepted_requests = user.accepted_requests 
            return render_template('dashboard.html', user=user, requests=user_requests, responses=user_responses, accepted_requests=accepted_requests)
        else:
            flash('User not found')
            return redirect(url_for('login'))
    else:
        flash('Please login first')
        return redirect(url_for('login'))



    

@app.route('/create_request', methods=['GET', 'POST'])
def create_request():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        
        if user_id and title and description:
            new_request = Request(title=title, description=description, user_id=user_id)
            db.session.add(new_request)
            db.session.commit()
            flash('Request created successfully.')
            return redirect(url_for('dashboard'))
        else:
            flash('Please fill all the fields.')
    return render_template('create_request_form.html', user = user)

@app.route('/search_requests', methods=['GET'])
def search_requests():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    query = request.args.get('query', '')
    search_results = []
    if query:
        search_results = Request.query.filter(Request.title.contains(query) | Request.description.contains(query)).all()
    return render_template('search_requests.html', search_results=search_results, user = user)



@app.route('/request_details/<int:request_id>', methods=['GET'])
def request_details(request_id):
    request = Request.query.get(request_id)
    if not request:
        flash('Request not found.')
        return redirect(url_for('search_requests'))

   # Get answers from all users who accepted the request
    accepted_responses = Response.query.filter_by(request_id=request_id).all()

    # Get the current user
    user_id = session.get('user_id')
    current_user = User.query.get(user_id) if user_id else None
    
    return render_template('request_details.html', request=request, accepted_responses=accepted_responses, current_user=current_user)


@app.route('/accept_request/<int:request_id>', methods=['GET'])
def accept_request(request_id):
    user_id = session.get('user_id')
    if not user_id:
        flash('You need to login first.', 'error')
        return redirect(url_for('login'))

    request_to_accept = Request.query.get(request_id)
    if not request_to_accept:
        flash('Request not found.', 'error')
        return redirect(url_for('search_requests'))

    current_user = User.query.get(user_id)
    if current_user in request_to_accept.accepted_by:
        # If the current user has accepted the request, display a flash message to remind the user not to accept the request again.
        flash('You have already accepted this request. Please do not accept it again.', 'info')
        return redirect(url_for('request_details', request_id=request_id,current_user=current_user))

    # If the current user has not accepted the request, add him to the recipient list and save
    request_to_accept.accepted_by.append(current_user)
    db.session.commit()
    flash('Request accepted successfully.', 'success')
    return redirect(url_for('request_details', request_id=request_id,current_user=current_user))




@app.route('/my_accepted_requests')
def my_accepted_requests():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        accepted_requests = user.accepted_requests  # This will fetch the accepted requests for the user
        return render_template('my_accepted_requests.html', user = user, accepted_requests=accepted_requests)
    else:
        flash('Please log in to view accepted requests.')
        return redirect(url_for('login'))





@app.route('/answer_request/<int:request_id>', methods=['GET'])
def answer_request(request_id):
    request = Request.query.get(request_id)
    
    if not request:
        flash('Request not found.')
        return redirect(url_for('dashboard'))

    user_id = session.get('user_id')
    if user_id is None:
        flash('Please log in to view the request details.')
        return redirect(url_for('login'))

    current_user = User.query.get(user_id)
    
    # Get all answers to this request
    responses = Response.query.filter_by(request_id=request_id).all()

    if current_user in request.accepted_by:
        return render_template('answer_request.html', request=request, responses=responses, current_user=current_user)
    else:
        flash('You have not accepted this request.')
        return redirect(url_for('dashboard'))


@app.route('/submit_answer/<int:request_id>', methods=['POST'])
def submit_answer(request_id):
    response_text = request.form.get('response')
    if response_text:
        #Create an answer instance and save it to the database
        new_response = Response(request_id=request_id, user_id=session.get('user_id'), response_text=response_text)
        db.session.add(new_response)
        db.session.commit()
        flash('Your answer was submitted successfully.')
    else:
        flash('Your answer cannot be empty.')

    return redirect(url_for('answer_request', request_id=request_id))

@app.route('/update_profile', methods=['GET', 'POST'])
def update_profile():
    form = UserProfileForm()
    user = User.query.get_or_404(session['user_id'])

    if form.validate_on_submit() and 'submit_update' in request.form:
        user.username = form.username.data
        user.email = form.email.data
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('update_profile'))

    return render_template('update_profile.html', form=form, user=user)

@app.route('/search_avatar', methods=['GET', 'POST'])
def search_avatar():
    form = UserProfileForm()  # May need to modify or use a different form to accommodate image-only searches
    user = User.query.get_or_404(session['user_id'])

    if request.method == 'POST' and 'submit_search' in request.form:
        images = search_pexels_images(form.image_search.data)
        if images:
            return render_template('search_avatar.html', form=form, images=images, user=user)
        else:
            flash('No images found. Try another search.', 'error')

    return render_template('search_avatar.html', form=form, user=user)

@app.route('/set_avatar')
def set_avatar():
    image_url = request.args.get('image_url')
    user_id = session['user_id']
    user = User.query.get(user_id)
    if user:
        user.avatar_url = image_url
        db.session.commit()
        flash('Avatar updated successfully!', 'success')
    return redirect(url_for('dashboard'))



@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.')
    return redirect(url_for('login'))