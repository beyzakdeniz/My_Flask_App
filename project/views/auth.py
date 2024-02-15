from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user, UserMixin
import re

from ..models import User
from .. import db

auth = Blueprint('auth', __name__)


# Function to check if a password meets complexity requirements
def is_valid_password(password):
    message = """Your password must be have at least
                    8 characters long
                    1 uppercase & 1 lowercase character
                    1 number"""
    return bool(re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', password)), message


# Function to check if an email address is valid
def is_valid_email(email):
    return bool(re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email))


@auth.route('/login')
def login():
    return render_template('authentication/login.html', user=current_user)


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()
    if user:
        if check_password_hash(user.password, password):
            flash('Logged in successfully!', category='success')
            login_user(user, remember=remember)
            current_user.last_login = datetime.utcnow()
            db.session.commit()
            return redirect(url_for('main.home'))
        else:
            flash('Incorrect password, try again.', category='error')
    else:
        flash('Email does not exist.', category='error')

    return redirect(url_for('auth.login'))


@auth.route('/signup')
def signup():
    return render_template('main/user_create.html', user=current_user)


@auth.route('/signup', methods=['GET', 'POST'])
def signup_post():
    if request.method == 'POST':
        # Get the data from the request body
        username = request.form['username']
        firstname = request.form['firstname']
        middlename = request.form['middlename']
        lastname = request.form['lastname']
        birthdate = request.form['birthdate']
        email = request.form['email']
        password1 = request.form['password1']
        password2 = request.form['password2']

        # check if email has been used before
        user = User.query.filter_by(email=email).first()

        # if a user is found, we want to redirect back to signup page so user can try again
        if user:
            flash('Email address already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(username) < 3:
            flash('Username must be greater than 2 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif not is_valid_password(password1)[0]:
            flash(is_valid_password(password1)[1], category='error')
        elif not is_valid_email(email):
            flash('Invalid email format!', category='error')
        else:
            new_user = User(username=username, firstname=firstname, middlename=middlename, lastname=lastname,
                        birthdate=birthdate, email=email, password=generate_password_hash(password1, method='scrypt'))
            db.session.add(new_user)
            db.session.commit()
            if not current_user:
                login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('main.home'))

    return redirect(url_for('auth.signup'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
