from flask import render_template, flash, request, redirect
from models import Users, Posts
from flask_login import login_required, login_user, logout_user

from __init__ import db, app, manager
from address_generator import create_address
from password_generator import create_password
from save_picture import save_images, save_main, check_type_images, check_type_main
from text_editor import text_editor
from image_editor import image_editor
from counter import counter

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
            flash('Пользователь уже существует', 'danger')
        else:
            password = create_password()
            print(password)
            user = Users(email=login, password=password, role='poster')
            db.session.add(user)
            db.session.commit()
            flash('Пользователь добавлен', 'success')
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
<<<<<<< HEAD
=======
                flash(f'Hello{user.email}', 'success')
>>>>>>> a0ed675aed43f254ef1706b2c98c02846467b2b3
                return redirect('/allposts')
        else:
            flash('Пользователь не существует', 'danger')

    return render_template('login.html')


@app.route('/post/<address>')
def post(address):
    post = Posts.query.filter_by(address=address).first()
    if post:
        text = post.text
        mini_text, notes = text_editor(text)
        images_list = image_editor(post.post_images)
        count = counter(mini_text)
    else:
        return redirect('/')
    return render_template('post.html', post=post, mini_text=mini_text, notes=notes, images=images_list, count=count)


@app.route('/createpost', methods=['POST', 'GET'])
@login_required
def create_post():
    if request.method == 'POST':
        main_image = request.files['main-image']
        header = request.form.get('header')
        text = request.form.get('text')
        images = request.files.getlist('images')
        address = create_address()
<<<<<<< HEAD

        if main_image:
            check_main = check_type_main(main_image)
            if check_main == True:
                main_image = save_main(main_image, address)
                if images:
                    check_images = check_type_images(images)
                    if check_images == True:
                        images = save_images(images, address)
                        post = Posts(address=address, header=header, text=text, main_image=main_image, post_images=images)
                        db.session.add(post)
                        db.session.commit()
                        flash('Пост создан', 'success')
                    else:
                        flash('Не допустимый тип у картинок в посте', 'danger')
                else:
                    post = Posts(address=address, header=header, text=text, main_image=main_image)
                    db.session.add(post)
                    db.session.commit()
                    flash('Пост создан', 'success')
=======
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
>>>>>>> a0ed675aed43f254ef1706b2c98c02846467b2b3
            else:
                flash('Основная картинка не может быть такого типа', 'danger')
        else:
<<<<<<< HEAD
            flash('Добавьте основную картинку', 'danger')



=======
            post = Posts(header=header, text=text, address=address)
            db.session.add(post)
            db.session.commit()
            print(f'success, {address}')
            flash('Пост создан', 'success')
>>>>>>> a0ed675aed43f254ef1706b2c98c02846467b2b3
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
