from flask import render_template, flash, request, redirect
from models import Users, Posts
from flask_login import login_required, login_user, current_user, logout_user

from __init__ import db, app, manager

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        user = Users.query.filter_by(email=login).first()
        if user:
            if user.password == password:
                login_user(user)
                flash(f'Hello{user.email}', 'success')
        else:
            flash('User dont exist', 'danger')

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
    user = Users.query.filter_by(email='admin').first()
    if user:
        pass
    else:
        user = Users(email='admin', password='1234')
        db.session.add(user)
        db.session.commit()
    db.create_all()
    app.run(host='0.0.0.0',port=8080,debug=True)
