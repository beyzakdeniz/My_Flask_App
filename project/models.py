from . import db
from flask_login import UserMixin


# Define the User model
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    firstname = db.Column(db.String(100), nullable=False)
    middlename = db.Column(db.String(100), nullable=True)
    lastname = db.Column(db.String(100), nullable=False)
    birthdate = db.Column(db.DateTime, nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    manager = db.Column('is_manager', db.Boolean(), nullable=False, server_default='0')
    last_active = db.Column(db.DateTime, nullable=True)
    last_login = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<User: {self.username}>'


class Item(UserMixin, db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    xp = db.Column(db.Integer, nullable=True)
    content = db.Column(db.Text, nullable=False)
    is_done = db.Column(db.Boolean(), nullable=False, default=False)

