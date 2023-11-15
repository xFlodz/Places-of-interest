from flask import render_template, flash, request, redirect
from models import Users, Posts
from flask_login import login_required, login_user, logout_user

from __init__ import db, app, manager
from address_generator import create_address
from password_generator import create_password
from save_picture import allowed_file

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['POST', 'GET'])
@login_required
def register():
    if request.method == 'POST':
        login = request.form.get('login')
        user = Users.query.filter_by(email=login).first()
        if user:
            flash('This user already exists', 'danger')
        else:
            password = create_password()
            print(password)
            user = Users(email=login, password=password, role='poster')
            db.session.add(user)
            db.session.commit()
    return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')


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
                return redirect('/allposts')
        else:
            flash('User dont exist', 'danger')

    return render_template('login.html')


@app.route('/post/<address>')
def post(address):
    post = Posts.query.filter_by(address=address).first()
    if post:
        pass
    else:
        return redirect('/')
    return render_template('post.html', post=post, post_image=post.image)


@app.route('/createpost', methods=['POST', 'GET'])
@login_required
def create_post():
    if request.method == 'POST':
        header = request.form.get('header')
        text = request.form.get('text')
        image = request.files['image']
        address = create_address()
        if image:
            check = allowed_file(image, address)
            if check == 1:
                filetype = image.filename.rsplit('.', 1)[1].lower()
                image = f'/static/post_images/{address}.{filetype}'
                post = Posts(header=header, text=text, image=image, address=address)
                db.session.add(post)
                db.session.commit()
                print(f'success', {address})
                flash('Пост создан', 'success')
            else:
                flash('Недопустимый тип файла')
        else:
            post = Posts(header=header, text=text, address=address)
            db.session.add(post)
            db.session.commit()
            print(f'success, {address}')
            flash('Пост создан', 'success')
    return render_template('create_post.html')

@app.route('/allposts')
@login_required
def all_posts():
    posts = Posts.query.all()
    return render_template('all_posts.html', posts=posts)


@manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


if __name__ == '__main__':
    db.create_all()
    user = Users.query.filter_by(email='admin').first()
    if user:
        pass
    else:
        user = Users(email='admin', password='1234', role='admin')
        user2 = Users(email='poster', password='1234', role='poster')
        db.session.add(user)
        db.session.add(user2)
        db.session.commit()
    app.run(host='0.0.0.0',port=8080,debug=True)
