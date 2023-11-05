from flask import render_template, flash
from models import Users, Posts
from flask_login import login_required

from __init__ import db, app, manager


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/post/<address>')
def post(address):
    return render_template('post.html')


@app.route('/createpost')
@login_required
def create_post():
    return render_template('create_post.html')

@app.route('/allposts')
@login_required
def all_posts():
    return render_template('all_posts.html')


@manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


if __name__ == '__main__':
    #db.create_all()
    app.run(host='0.0.0.0',port=8080,debug=True)
