# edited by paolo
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, TextAreaField, IntegerField, FloatField, SelectField, DateField, TimeField
from wtforms.validators import InputRequired, Email, EqualTo, NumberRange, Optional, Length

# creates the login information
class LoginForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired('Enter user name')])
    password = PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

# this is the registration form
class RegisterForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired()])
    email = StringField("Email Address", validators=[Email("Please enter a valid email")])
    first_name = StringField("First Name", validators=[InputRequired()])
    surname = StringField("Surname", validators=[InputRequired()])
    contact_number = StringField("Contact Number", validators=[InputRequired()])
    street_address = StringField("Street Address", validators=[InputRequired()])
    
    # linking two fields - password should be equal to data entered in confirm
    password = PasswordField("Password", validators=[InputRequired(), EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")
    
    # submit button
    submit = SubmitField("Register")

# Event Creation Form
class EventForm(FlaskForm):
    title = StringField("Event Title", validators=[InputRequired()])
    category = SelectField("Category", choices=[('FPS', 'FPS'), ('MOBA', 'MOBA'), ('RPG', 'RPG'), ('Fighting', 'Fighting')], validators=[InputRequired()])
    description = TextAreaField("Description", validators=[InputRequired()])
    date = DateField("Date", validators=[InputRequired()])
    start_time = TimeField("Start Time", validators=[InputRequired()])
    end_time = TimeField("End Time", validators=[InputRequired()])
    venue = StringField("Venue", validators=[InputRequired()])
    image_url = StringField("Image URL", validators=[Optional()])
    ticket_price = FloatField("Ticket Price", validators=[InputRequired(), NumberRange(min=0)])
    tickets_available = IntegerField("Tickets Available", validators=[InputRequired(), NumberRange(min=1)])
    acknowledgement = SelectField("Acknowledgement of Country", choices=[('None', 'None'), ('Generic', 'Generic'), ('Enhanced', 'Enhanced')], validators=[InputRequired()])
    acknowledgement_text = TextAreaField("Enhanced Acknowledgement of Country (optional)", validators=[Optional(), Length(max=500)])
    submit = SubmitField("Create Event")

# Booking Form
class BookingForm(FlaskForm):
    quantity = IntegerField("Number of Tickets", validators=[InputRequired(), NumberRange(min=1)])
    submit = SubmitField("Book Tickets")

# Comment Form
class CommentForm(FlaskForm):
    text = TextAreaField("Comment", validators=[InputRequired()])
    submit = SubmitField("Post Comment")
