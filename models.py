from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


class Users(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    token = db.Column(db.Text)
    email = db.Column(db.Text)
    direction = db.Column(db.Text)
    level = db.Column(db.Integer)
    is_banned = db.Column(db.Integer)
    is_hidden = db.Column(db.Integer)
    is_admin = db.Column(db.Integer)


class Reports(db.Model):
    __tablename__ = "Reports"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    week = db.Column(db.Integer)
    content = db.Column(db.Text, default="")
    date = db.Column(db.Date, default=datetime.datetime.utcnow)


class Configs(db.Model):
    __tablename__ = "Configs"
    id = db.Column(db.Integer, primary_key=True)
    begin_week = db.Column(db.Integer)
    skip_weeks = db.Column(db.Text)
