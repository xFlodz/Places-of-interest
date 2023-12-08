from flask import render_template, flash, request, redirect
from models import Users, Posts, Tags, PostTags
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from __init__ import db, app, manager
from address_generator import create_address
from password_generator import create_password
from save_picture import save_image, save_main, check_type_image, update_images
from text_editor import text_editor, get_notes
from image_editor import image_editor
from counter import counter
from delete_images import delete_images, delete_main
from mail_sender import mailsend

@app.route('/')
def index():
    return redirect('/allposts')


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


@app.route('/tags', methods=['POST', 'GET'])
@login_required
def add_tag():
    tags = Tags.query.all()
    if request.method == 'POST':
        tag = request.form.get('tag')
        if tag:
            check_tag = Tags.query.filter_by(nametag=tag).first()
            if check_tag:
                flash('Такой тег уже существует', 'danger')
            else:
                new_tag = Tags(nametag=tag)
                db.session.add(new_tag)
                db.session.commit()
                flash('Тег успешно добавлен', 'success')
        else:
            flash('Введите тег', 'danger')
    return render_template('add_tags.html', tags=tags)


@app.route('/delete_tags/<tag>')
@login_required
def delete_tags_id(tag):
    posts_with_this_tag = PostTags.query.filter_by(tag=tag).all()
    tag_in_db = Tags.query.filter_by(nametag=tag).first()
    db.session.delete(tag_in_db)
    for post in posts_with_this_tag:
        tag_post = PostTags.query.filter_by(tag=tag).first()
        db.session.delete(tag_post)
    db.session.commit()
    return redirect('/add_tag')


@app.route('/delete_tags', methods=['GET', 'POST'])
@login_required
def delete_tags():
    tags = Tags.query.all()
    return render_template('delete_tags.html', tags=tags)


@app.route('/delete_tags/<tag>')
@login_required
def delete_tags_id(tag):
    posts_with_this_tag = PostTags.query.filter_by(tag=tag).all()
    print(posts_with_this_tag)
    tag_in_db = Tags.query.filter_by(nametag=tag).first()
    print(tag)
    db.session.delete(tag_in_db)
    for post in posts_with_this_tag:
        tag_post = PostTags.query.filter_by(tag=tag).first()
        db.session.delete(tag_post)
    db.session.commit()
    return redirect('/')


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
        mini_text = text_editor(text)
        images_list = post.post_images
        count = counter(mini_text)
        notes = get_notes(images_list, post.address)
        images_list = image_editor(post.post_images)
        tags = PostTags.query.filter_by(address=address).all()
        tags_list = []
        for tag in tags:
            tags_list.append(tag.tag)
    else:
        return redirect('/')
    return render_template('post.html', post=post, mini_text=mini_text, notes=notes, images=images_list, count=count, tags=tags_list)


@app.route('/createpost', methods=['POST', 'GET'])
@login_required
def create_post():
    tags = Tags.query.all()
    if request.method == 'POST':
        main_image = request.files['main-image']
        header = request.form.get('header')
        text = request.form.get('text')
        address = create_address()
        for tag in tags:
            if request.form.get(f'{tag.nametag}'):
                post_tag = PostTags(address=address, tag=tag.nametag)
                db.session.add(post_tag)
                db.session.commit()
        if header:
            if text:
                if main_image:
                    check_main = check_type_image(main_image)
                    if check_main == True:
                        main_image = save_main(main_image, address)
                        visible = 'no'
                        post = Posts(address=address, header=header, text=text, main_image=main_image, visible=visible)
                        db.session.add(post)
                        db.session.commit()
                        return redirect(f'/confirmpost/{post.address}')
                    else:
                        flash('Основная картинка не может быть такого типа', 'danger')
                else:
                    flash('Добавьте основную картинку', 'danger')
            else:
                flash('Добавьте в пост текст', 'danger')
        else:
            flash('Добавьте в пост заголовок', 'danger')



    return render_template('create_post.html', tags=tags)


@app.route('/confirmpost/<address>', methods=['POST', 'GET'])
@login_required
def confirm_post(address):
    tags = PostTags.query.filter_by(address=address).all()
    tags_list = []
    for tag in tags:
        tags_list.append(tag.tag)
    post = Posts.query.filter_by(address=address).first()
    text = post.text
    mini_text = text_editor(text)
    count = counter(mini_text)
    count_for_image = text.count('$')
    if request.method == 'POST':
        notes = []
        images = []
        for i in range(count_for_image):
            note = request.form.get(f'note{i}')
            image = request.files[f'image{i}']
            if image:
                check = check_type_image(image)
                if check == False:
                    flash(f'Неподходящий тип картинки {i+1}', 'danger')
                else:
                    name = save_image(image, post.address, i)
                    images.append(name)
            if len(note) > 155:
                flash('Описание больше 155 символов', 'danger')
            else:
                notes.append(note)
        if count_for_image == len(notes):
            if count_for_image == len(images):
                names = update_images(notes, images)
                post.post_images = names
                post.visible = 'yes'
                db.session.commit()
                return redirect(f'/post/{address}')
            else:
                flash('Добавьте картинки', 'danger')
        else:
            flash('Добавьте описания', 'danger')
    return render_template('confirm_post.html', post=post, mini_text=mini_text, count=count, count_for_image=count_for_image-1, tags=tags_list)


@app.route('/editpost/<address>', methods=['POST', 'GET'])
@login_required
def edit_post(address):
    tags = Tags.query.all()
    tags_list = []
    tags_in_this_post_list = []
    for i in tags:
        tags_list.append(i.nametag)
    tags_in_this_post = PostTags.query.filter_by(address=address).all()
    for i in tags_in_this_post:
        tags_in_this_post_list.append(i.tag)
    post = Posts.query.filter_by(address=address).first()
    new_tags = []
    if request.method == 'POST':
        for tag in tags:
            if request.form.get(f'{tag.nametag}'):
                new_tags.append(tag.nametag)
        if len(new_tags) >= 1:
            delete_tags = PostTags.query.filter_by(address=address).all()
            if delete_tags:
                for i in delete_tags:
                    db.session.delete(i)
                    db.session.commit()
            for i in new_tags:
                post_tag = PostTags(address=address, tag=i)
                db.session.add(post_tag)
                db.session.commit()
        else:
            delete_tags = PostTags.query.filter_by(address=address).all()
            for i in delete_tags:
                db.session.delete(i)
                db.session.commit()
        main_image = request.files['main-image']
        header = request.form.get('header')
        text = request.form.get('text')
        error = False
        if main_image:
            check = check_type_image(main_image)
            if check == True:
                delete_main(post)
                new_main_image = save_main(main_image, post.address)
                post.main_image = new_main_image
            else:
                error = True
        if text:
            post.text = text
        if header:
            post.header = header
        if error == False:
            db.session.commit()
            return redirect(f'/confirmedit/{address}')
        else:
            flash('Картинка не может быть такого типа', 'danger')
    return render_template('edit_post.html', post=post, tags=tags_list, titps=tags_in_this_post_list)


@app.route('/confirmedit/<address>', methods=['POST', 'GET'])
@login_required
def confirm_edit(address):
    tags = PostTags.query.filter_by(address=address).all()
    tags_list = []
    for tag in tags:
        tags_list.append(tag.tag)
    post = Posts.query.filter_by(address=address).first()
    text = post.text
    mini_text = text_editor(text)
    count = counter(mini_text)
    count_for_image = text.count('$')
    if request.method == 'POST':
        notes = []
        images = []
        for i in range(count_for_image):
            note = request.form.get(f'note{i}')
            image = request.files[f'image{i}']
            if image:
                check = check_type_image(image)
                if check == False:
                    flash(f'Неподходящий тип картинки {i+1}', 'danger')
                else:
                    name = save_image(image, post.address, i)
                    images.append(name)
            if len(note) > 155:
                flash('Описание больше 155 символов', 'danger')
            else:
                notes.append(note)
        if count_for_image == len(notes):
            if count_for_image == len(images):
                delete_images(post)
                names = update_images(notes, images)
                post.post_images = names
                post.visible = 'yes'
                db.session.commit()
                return redirect(f'/post/{address}')
            else:
                flash('Добавьте картинки', 'danger')
        else:
            flash('Добавьте описания', 'danger')
    return render_template('confirm_edit.html', post=post, mini_text=mini_text, count=count, count_for_image=count_for_image-1, tags=tags_list)


@app.route('/deletepost/<address>')
@login_required
def delete_post(address):
    post = Posts.query.filter_by(address=address).first()
    delete_images(post)
    delete_main(post)
    db.session.delete(post)
    db.session.commit()
    return redirect('/allposts')


@app.route('/allposts', methods=['POST', 'GET'])
def all_posts():
    posts = Posts.query.all()
    tags = Tags.query.all()
    tags_list = []
    filtered_posts = []
    post_list = []
    if request.method == 'POST':
        for tag in tags:
            if request.form.get(f'{tag.nametag}'):
                tags_list.append(tag.nametag)

    if tags_list:
        if len(tags_list) == 1:
            for tag in tags_list:
                post_tags = PostTags.query.filter_by(tag=tag).all()
                for post in post_tags:
                    post_list.append(post)
        else:
            post_list_non_filtered = []
            post_list_filtered = []
            for tag in tags_list:
                post_tags = PostTags.query.filter_by(tag=tag).all()
                for post in post_tags:
                    post_list_non_filtered.append(post.address)
            for i in post_list_non_filtered:
                if post_list_non_filtered.count(i) == len(tags_list):
                    if i not in post_list_filtered:
                        post_list_filtered.append(i)
            for i in post_list_filtered:
                post_add = PostTags.query.filter_by(address=i).first()
                post_list.append(post_add)

    if post_list:
        for post in post_list:
            post_add = Posts.query.filter_by(address=post.address).first()
            filtered_posts.append(post_add)

    if request.method == 'POST':
        if filtered_posts:
            print(filtered_posts)
            if filtered_posts != [None]:
                posts = filtered_posts
            else:
                flash('Постов с таким тегом не существует', 'danger')
        else:
            flash('Постов с таким набором тегов нет', 'danger')

    return render_template('all_posts.html', posts=posts, tags=tags)


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
