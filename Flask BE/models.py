from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from flask import current_app as app


db=SQLAlchemy()


role_users = db.Table('role_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class User(db.Model,UserMixin):
  __tablename__ = 'user'
  id = db.Column(db.Integer, primary_key = True)
  email = db.Column(db.String(255), unique=True)
  name = db.Column(db.String, unique=True)
  password = db.Column(db.String(255))
  active = db.Column(db.Boolean())
  fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False,) 
  roles = db.relationship('Role', secondary=role_users,backref=db.backref('users', lazy='dynamic'))


class Role(db.Model,RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))




class Lists(db.Model):
    __tablename__ = 'lists'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    u_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    cards = db.relationship('Cards', backref='card')


class Cards(db.Model):
    __tablename__ = 'cards'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    time_created = db.Column(db.DateTime)
    time_updated = db.Column(db.DateTime)
    time_completed = db.Column(db.DateTime, default=None)
    deadline = db.Column(db.DateTime)
    completed_flag = db.Column(db.Boolean)
    l_id = db.Column(db.Integer, db.ForeignKey('lists.id'), nullable=False)

