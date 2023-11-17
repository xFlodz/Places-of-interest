from flask import render_template, flash, request, redirect
from models import Users, Posts
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from __init__ import db, app, manager
from address_generator import create_address
from password_generator import create_password
from save_picture import save_images, save_main, check_type_images, check_type_main
from text_editor import text_editor
from image_editor import image_editor
from counter import counter
from delete_images import delete_images
from mail_sender import mailsend

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
            flash(f'Пароль {password}', 'success')
            mailsend(login, password)
            password = generate_password_hash(password)
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
            if check_password_hash(user.password, password):
                login_user(user)
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

        if header:
            if text:
                if main_image:
                    check_main = check_type_main(main_image)
                    if check_main == True:
                        main_image = save_main(main_image, address)
                        if images[0]:
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
                    else:
                        flash('Основная картинка не может быть такого типа', 'danger')
                else:
                    flash('Добавьте основную картинку', 'danger')
            else:
                flash('Добавьте в пост текст', 'danger')
        else:
            flash('Добавьте в пост заголовок', 'danger')



    return render_template('create_post.html')


@app.route('/editpost/<address>', methods=['POST', 'GET'])
@login_required
def edit_post(address):
    post = Posts.query.filter_by(address=address).first()
    if request.method == 'POST':
        pass
    return render_template('edit_post.html', post=post)


@app.route('/deletepost/<address>')
@login_required
def delete_post(address):
    post = Posts.query.filter_by(address=address).first()
    delete_images(post)
    db.session.delete(post)
    db.session.commit()
    return redirect('/')


@app.route('/allposts')
@login_required
def all_posts():
    posts = Posts.query.all()
    return render_template('all_posts.html', posts=posts)


@manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)

def error(e):
    return render_template('error.html')


app.register_error_handler(404, error)
app.register_error_handler(401, error)


if __name__ == '__main__':
    db.create_all()
    user = Users.query.filter_by(email='admin').first()
    if user:
        pass
    else:
        password = generate_password_hash('1234')
        user = Users(email='admin', password=password, role='admin')
        user2 = Users(email='poster', password=password, role='poster')
        db.session.add(user)
        db.session.add(user2)
        db.session.commit()
    app.run(host='0.0.0.0',port=8080,debug=True)
