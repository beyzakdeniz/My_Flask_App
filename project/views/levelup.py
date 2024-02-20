from datetime import datetime, timedelta

from flask import render_template, request, url_for, redirect, flash, Blueprint
from flask_login import login_required, current_user
from ..models import User, Item
from .. import db


levelup = Blueprint('levelup', __name__)


@levelup.route('/levelup')
@login_required
def profile():
    return render_template('levelup/profile.html', user=current_user)


@levelup.route('/levelup/list')
@login_required
def item_list():
    items = Item.query.all()
    return render_template('levelup/item_list.html', user=current_user, items=items)


@levelup.route('/levelup/create', methods=('GET', 'POST'))
@login_required
def item_create():
    if request.method == 'POST':
        # Get the data from the request body
        xp = request.form['xp']
        content = request.form['content']

        new_item = Item(xp=xp, content=content)
        db.session.add(new_item)
        db.session.commit()
        flash('Item created!', category='success')
        return redirect(url_for('levelup.item_list'))

    return render_template('levelup/item_create.html', user=current_user)


@levelup.post('/levelup/delete/<int:id>')
@login_required
def item_delete(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('levelup.profile'))

