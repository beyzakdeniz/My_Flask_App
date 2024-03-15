from datetime import datetime, timedelta

from flask import render_template, request, url_for, redirect, flash, Blueprint
from flask_login import login_required, current_user
from ..models import User
from .. import db


main = Blueprint('main', __name__)


@main.route('/')
@login_required
def home():
    return render_template('main/home.html', user=current_user)


@main.route('/user/list')
@login_required
def user_list():
    users = User.query.all()
    return render_template('main/user_list.html', users=users, user=current_user)


@main.route('/user/create', methods=('GET', 'POST'))
@login_required
def user_create():
    return redirect(url_for('auth.signup_post'))


@main.route('/user/update/<int:idx>', methods=('GET', 'POST'))
@login_required
def user_update(idx):
    user = User.query.get_or_404(idx)
    if request.method == 'POST':
        username = request.form.get('username')
        firstname = request.form.get('firstname')
        middlename = request.form.get('middlename')
        lastname = request.form.get('lastname')
        birthdate = request.form.get('birthdate')
        email = request.form.get('email')

        print(username,
        firstname,
        middlename,
        lastname,
        birthdate,
        email)

        user.username = username
        user.firstname = firstname
        user.middlename = middlename
        user.lastname = lastname
        user.birthdate = birthdate
        user.email = email

        db.session.add(user)
        db.session.commit()
        flash('User data updated successfully.', category='success')
        return redirect(url_for('main.user_list'))

    return render_template('main/user_update.html', user=user)


@main.post('/user/delete/<int:id>')
@login_required
def user_delete(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('main.home'))


@main.route('/onlineusers', methods=('GET', 'POST'))
@login_required
# @admin_required
def online_users():
    online_users = []
    users = User.query.all()
    for user in users:
        if user.last_active and (datetime.utcnow() - user.last_active < timedelta(minutes=1)):
            online_users.append(user)

    return render_template('main/onlineusers.html', online_users=online_users, user=current_user)


@main.before_request
def update_last_active():
    current_user.last_active = datetime.utcnow()
    db.session.commit()
