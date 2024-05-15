from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class UserProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email(message='Invalid email address'), Length(max=100)])
    image_search = StringField('Search for an avatar', validators=[Length(max=100)])
    submit_update = SubmitField('Update Profile')  # Used to update user information
    submit_search = SubmitField('Search Avatar')   # Used to search for avatars
