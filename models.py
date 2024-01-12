from __init__ import db
from flask_login import UserMixin


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String)


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(50), nullable=False, unique=True)
    header = db.Column(db.String(100), nullable=False)
    text = db.Column(db.String, nullable=False)
    main_image = db.Column(db.String, nullable=False)
    visible = db.Column(db.String(10), nullable=False)
    creator = db.Column(db.String)
    creation_time = db.Column(db.String, nullable=False)
    left_date = db.Column(db.String)
    right_date = db.Column(db.String)


class Tags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nametag = db.Column(db.String)


class PostTags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(50), nullable=False)
    tag = db.Column(db.String, nullable=False)


class PostImages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(50), nullable=False)
    path_to_image = db.Column(db.String, nullable=False)
    note = db.Column(db.String, nullable=False)


class PostVideo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(50), nullable=False)
    video_address = db.Column(db.String, nullable=False)