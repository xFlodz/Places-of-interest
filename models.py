from __init__ import db
from flask_login import UserMixin


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(50), nullable=False, unique=True)
    header = db.Column(db.String(100), nullable=False)
    text = db.Column(db.String, nullable=False)
    main_image = db.Column(db.String, nullable=False)
    post_images = db.Column(db.Text)
    visible = db.Column(db.String(10), nullable=False)


class Tags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nametag = db.Column(db.Text)


class PostTags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(50), nullable=False)
    tag = db.Column(db.Text, nullable=False)