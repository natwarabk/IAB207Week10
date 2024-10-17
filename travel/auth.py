from flask import Blueprint, render_template, redirect, url_for, flash
from .forms import LoginForm, RegisterForm
from flask_login import login_user, login_required, logout_user
from flask_bcrypt import generate_password_hash, check_password_hash
from .models import User
from . import db

# Create a blueprint for authentication
authbp = Blueprint('auth', __name__)

@authbp.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    # If the form is validated successfully (HTTP POST)
    if register_form.validate_on_submit():
        # Get username, password, and email from the form
        uname = register_form.user_name.data
        pwd = register_form.password.data
        email = register_form.email_id.data
        # Check if a user with the given username already exists
        user = db.session.scalar(db.select(User).where(User.name == uname))
        if user:  # If user exists
            flash('Username already exists, please try another')
            return redirect(url_for('auth.register'))
        # Hash the password to store securely
        pwd_hash = generate_password_hash(pwd).decode('utf-8')
        # Create a new User model object
        new_user = User(name=uname, password_hash=pwd_hash, emailid=email)
        # Add the user to the session and commit to the database
        db.session.add(new_user)
        db.session.commit()
        # Redirect to the main index page
        return redirect(url_for('main.index'))
    # If it's a GET request, render the registration page
    return render_template('user.html', form=register_form, heading='Register')

@authbp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    error = None
    if login_form.validate_on_submit():
        # Get the username and password from the form
        user_name = login_form.user_name.data
        password = login_form.password.data
        # Check if a user with the given username exists
        user = db.session.scalar(db.select(User).where(User.name == user_name))
        # If no user exists with that name
        if user is None:
            error = 'Incorrect username'  # Security note: be careful with detailed errors
        # Check the password using hash comparison
        elif not check_password_hash(user.password_hash, password):
            error = 'Incorrect password'
        # If no error, login the user
        if error is None:
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            flash(error)
    # Render the login page if there are errors or it's a GET request
    return render_template('user.html', form=login_form, heading='Login')

@authbp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
