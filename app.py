from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'CITS5505'
db = SQLAlchemy(app)
migrate = Migrate(app, db)




#Database
#Create association table
accepted_requests = db.Table('accepted_requests',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('request_id', db.Integer, db.ForeignKey('request.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    accepted_requests = db.relationship('Request', secondary=accepted_requests, lazy='subquery',backref=db.backref('accepted_by', lazy=True))
    responses = db.relationship('Response', backref='responder', lazy=True) 

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    status = db.Column(db.String(10), default='open')


class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('request.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    response_text = db.Column(db.Text, nullable=False)






# Routes


@app.route('/')
def home():
    return render_template('introductory.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    error_message = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        elif user:
            error_message = 'Incorrect password.'
        else:
            error_message = 'User not found.'

    return render_template('login.html', error_message=error_message)





@app.route('/register', methods=['POST', 'GET'])
def register():
    error_message = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            error_message = 'Username already taken. Please choose another one.'
        else:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))

    return render_template('register.html', error_message=error_message)

@app.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        if user:
            user_requests = Request.query.filter_by(user_id=user_id).all()
            user_responses = Response.query.filter_by(user_id=user_id).all()
            return render_template('dashboard.html', user=user, requests=user_requests, responses=user_responses)
        else:
            flash('User not found')
            return redirect(url_for('login'))
    else:
        flash('Please login first')
        return redirect(url_for('login'))
    

@app.route('/create_request', methods=['GET', 'POST'])
def create_request():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        user_id = session.get('user_id')
        if user_id and title and description:
            new_request = Request(title=title, description=description, user_id=user_id)
            db.session.add(new_request)
            db.session.commit()
            flash('Request created successfully.')
            return redirect(url_for('dashboard'))
        else:
            flash('Please fill all the fields.')
    return render_template('create_request_form.html')

@app.route('/search_requests', methods=['GET'])
def search_requests():
    query = request.args.get('query', '')
    search_results = []
    if query:
        search_results = Request.query.filter(Request.title.contains(query) | Request.description.contains(query)).all()
    return render_template('search_requests.html', search_results=search_results)



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
        return redirect(url_for('request_details', request_id=request_id))

    # If the current user has not accepted the request, add him to the recipient list and save
    request_to_accept.accepted_by.append(current_user)
    db.session.commit()
    flash('Request accepted successfully.', 'success')
    return redirect(url_for('request_details', request_id=request_id))




@app.route('/my_accepted_requests')
def my_accepted_requests():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        accepted_requests = user.accepted_requests  # This will fetch the accepted requests for the user
        return render_template('my_accepted_requests.html', accepted_requests=accepted_requests)
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
    current_user = User.query.get(user_id)
    
    if current_user in request.accepted_by:
        return render_template('answer_request.html', request=request)
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




@app.route('/logout')
def logout():
    # Clear user information in the session
    session.pop('user_id', None) # Assume 'user_id' is the user ID stored in the session
    flash('You have been logged out.')
    return redirect(url_for('login'))  # Redirect to login page



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)




