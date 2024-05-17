from flask import render_template, request, redirect, url_for, flash, session
from app.models import db, User, Request, Response
from . import bp as requests_bp
from flask_login import login_required, login_user, logout_user, current_user

from .forms import CreateRequestForm


@requests_bp.route('/create_request', methods=['GET', 'POST'])
@login_required
def create_request():
    form = CreateRequestForm()
    if form.validate_on_submit():
        new_request = Request(
            title=form.title.data,
            description=form.description.data,
            user_id=current_user.id  
        )
        db.session.add(new_request)
        db.session.commit()
        flash('Request created successfully.', 'success')
        return redirect(url_for('dashboard.dashboard'))
    return render_template('requests/create_request_form.html', form=form)

@requests_bp.route('/search_requests', methods=['GET'])
@login_required
def search_requests():
    query = request.args.get('query', '')
    search_results = []
    if query:
        search_results = Request.query.filter(Request.title.contains(query) | Request.description.contains(query)).all()
    return render_template('requests/search_requests.html', search_results=search_results, user=current_user)


@requests_bp.route('/request_details/<int:request_id>', methods=['GET'])
@login_required
def request_details(request_id):
    request = Request.query.get(request_id)
    if not request:
        flash('Request not found.')
        return redirect(url_for('requests.search_requests'))

    # Get responses from all users who accepted this request
    accepted_responses = Response.query.filter_by(request_id=request_id).all()

    return render_template('requests/request_details.html', request=request, accepted_responses=accepted_responses, current_user=current_user)



@requests_bp.route('/accept_request/<int:request_id>', methods=['GET'])
@login_required
def accept_request(request_id):
    if not current_user.is_authenticated:
        flash('You need to login first.', 'error')
        return redirect(url_for('auth.login'))

    request_to_accept = Request.query.get(request_id)
    if not request_to_accept:
        flash('Request not found.', 'error')
        return redirect(url_for('requests.search_requests'))

    if current_user in request_to_accept.accepted_by:
        flash('You have already accepted this request. Please do not accept it again.', 'info')
        return redirect(url_for('requests.request_details', request_id=request_id))

    request_to_accept.accepted_by.append(current_user)
    db.session.commit()
    flash('Request accepted successfully.', 'success')
    return redirect(url_for('requests.request_details', request_id=request_id))





@requests_bp.route('/my_accepted_requests')
@login_required
def my_accepted_requests():
    # Use current_user to directly access logged in user information
    accepted_requests = current_user.accepted_requests  # Directly obtain the accepted request of the current user
    return render_template('requests/my_accepted_requests.html', user=current_user, accepted_requests=accepted_requests)


@requests_bp.route('/answer_request/<int:request_id>', methods=['GET'])
@login_required
def answer_request(request_id):
    request = Request.query.get(request_id)
    if not request:
        flash('Request not found.')
        return redirect(url_for('requests.search_requests'))

    # Use current_user to check if the user has accepted the request
    if current_user in request.accepted_by:
        responses = Response.query.filter_by(request_id=request_id).all()
        return render_template('requests/answer_request.html', request=request, responses=responses, current_user=current_user)
    else:
        flash('You have not accepted this request.')
        return redirect(url_for('dashboard.dashboard'))




@requests_bp.route('/submit_answer/<int:request_id>', methods=['POST'])
@login_required
def submit_answer(request_id):
    response_text = request.form.get('response')
    if response_text:
        #Create an answer instance and save it to the database
        new_response = Response(request_id=request_id, user_id=current_user.id, response_text=response_text)
        db.session.add(new_response)
        db.session.commit()
        flash('Your answer was submitted successfully.')
    else:
        flash('Your answer cannot be empty.')

    return redirect(url_for('requests.answer_request', request_id=request_id))

