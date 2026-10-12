# edited by paolo
from flask import Blueprint, flash, render_template, request, url_for, redirect
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .models import User
from .forms import LoginForm, RegisterForm
from . import db

# Create a blueprint - make sure all BPs have unique names
auth_bp = Blueprint('auth', __name__)

# this is a hint for a login function
@auth_bp.route('/login', methods=['GET', 'POST'])
# view function
def login():
    login_form = LoginForm()
    error = None
    if login_form.validate_on_submit():
        user_name = login_form.user_name.data
        password = login_form.password.data
        user = db.session.scalar(db.select(User).where(User.name == user_name))
        if user is None:
            error = 'Incorrect user name'
        elif not check_password_hash(user.password_hash, password): # takes the hash and cleartext password
            error = 'Incorrect password'
        if error is None:
            login_user(user)
            nextp = request.args.get('next') # this gives the url from where the login page was accessed
            if nextp is None or not nextp.startswith('/'):
                return redirect(url_for('views.index'))
            return redirect(nextp)
        else:
            flash(error)
    return render_template('user.html', form=login_form, heading='Login')

# this is the registration function
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        user_name = register_form.user_name.data
        email = register_form.email.data
        
        # Check if username or email already exists
        existing_user = db.session.scalar(db.select(User).where(
            (User.name == user_name) | (User.email == email)
        ))
        
        if existing_user:
            if existing_user.name == user_name:
                flash('Username already taken. Please choose another one.', 'danger')
            else:
                flash('Email already registered. Please login or use another email.', 'danger')
            return render_template('user.html', form=register_form, heading='Register')
        
        # If no existing user, proceed with creating the account
        password = register_form.password.data
        password_hash = generate_password_hash(password).decode('utf-8')
        
        new_user = User(
            name=user_name,
            email=email,
            password_hash=password_hash,
            first_name=register_form.first_name.data,
            surname=register_form.surname.data,
            contact_number=register_form.contact_number.data,
            street_address=register_form.street_address.data
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('views.index'))
        
    return render_template('user.html', form=register_form, heading='Register')

# this is the logout function
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.index'))