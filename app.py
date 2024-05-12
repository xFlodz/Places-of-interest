from flask import render_template, flash, request, redirect, abort, send_file, current_app
from models import Users, Posts, Tags, PostTags, PostImages, PostVideo, QRCode, GeoQuest, SaveGeoQuestProgress
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import desc
import base64
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from io import BytesIO
from __init__ import db, app, manager
from address_generator import create_address
from password_generator import create_password
from save_picture import save_image, save_main, check_type_image, upload_images
from text_editor import get_notes, edit_text, put_notes
from image_editor import image_editor
from counter import counter, id_counter
from delete_images import delete_images, delete_main
from mail_sender import mailsend
from current_date import date
from post_sort import post_sort
from video import get_html, check_video
from list_create import create_images_list, create_videos_list
from qr_code import qrcode_generate



@app.route('/')
def index():
    return redirect('/allposts')


@app.route('/register', methods=['POST', 'GET'])
@login_required
def register():
    if request.method == 'POST':
        login = request.form.get('login')
        name = request.form.get('name')
        surname = request.form.get('surname')
        thirdname = request.form.get('thirdname')
        if login == '' or '@' not in login:
            flash('Введите логин', 'danger')
        elif surname == '':
            flash('Введите Фамилию', 'danger')
        elif name == '':
            flash('Введите Имя', 'danger')
        elif thirdname == '':
            flash('Введите Отчество', 'danger')
        else:
            user = Users.query.filter_by(email=login).first()
            if user:
                flash('Пользователь уже существует', 'danger')
            else:
                password = create_password()
                flash(f'Пароль {password}', 'success')
                mailsend(login, password)
                password = generate_password_hash(password)
                user = Users(email=login, password=password, role='poster', name=name, surname=surname,
                             thirdname=thirdname)
                db.session.add(user)
                db.session.commit()
    return render_template('register.html')


@app.route('/account', methods=['POST', 'GET'])
@login_required
def account():
    name = current_user.name
    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')
        thirdname = request.form.get('thirdname')
        current_user.name, current_user.surname, current_user.thirdname = name, surname, thirdname
        db.session.commit()
        flash('Вы успешно изменили имя', 'success')
        return redirect('/account')
    return render_template('account.html')



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
                return redirect('/tags')
        else:
            flash('Введите тег', 'danger')
    return render_template('tags.html', tags=tags)


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
    return redirect('/tags')


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


@app.route('/timeline', methods=['POST', 'GET'])
def timeline():
    posts = Posts.query.order_by(Posts.left_date).all()
    lines = []
    for i in range(1700, 2041, 20):
        lines.append(i)

    posts_for_sort = posts.copy()
    sorted_lines = {}
    for line in lines:
        this_line_posts = []
        for post in posts_for_sort:
            if int(post.left_date[:4]) <= line:
                this_line_posts.append(post)
                posts_for_sort.remove(post)
        sorted_lines[f'{line}'] = this_line_posts

    new_sorted_lines = {}
    for key in sorted_lines:
        if len(sorted_lines[key]) >= 1:
            for post in sorted_lines[key]:
                if post.visible == 'yes':
                    new_sorted_lines[key] = sorted_lines[key]
                    break
    print(new_sorted_lines)

    start_text = []
    for k,v in new_sorted_lines.items():
        if v is not None:
            for post in v:
                new_text = edit_text(post.text)
                first_100_letters = f'{new_text[0][:100]}...'
                start_text.append(first_100_letters)
    return render_template('timeline.html', sorted_lines=new_sorted_lines, start_text=start_text)


@app.route('/timeline/<date>', methods=['POST', 'GET'])
def timeline_range(date):
    posts = Posts.query.order_by(Posts.left_date).all()
    lines = []
    for i in range(int(date), int(date)+100, 20):
        lines.append(i)

    posts_for_sort = posts.copy()
    sorted_lines = {}
    for line in lines:
        this_line_posts = []
        for post in posts_for_sort:
            if int(post.left_date[:4]) <= line:
                this_line_posts.append(post)
                posts_for_sort.remove(post)
        sorted_lines[f'{line}'] = this_line_posts


    new_sorted_lines = {}
    for key in sorted_lines:
        if len(sorted_lines[key]) >= 1:
            for post in sorted_lines[key]:
                if post.visible == 'yes':
                    new_sorted_lines[key] = sorted_lines[key]
                    break
    print(new_sorted_lines)

    start_text = []
    for k,v in new_sorted_lines.items():
        if v is not None:
            for post in v:
                new_text = edit_text(post.text)
                first_100_letters = f'{new_text[0][:100]}...'
                start_text.append(first_100_letters)
    return render_template('timeline.html', sorted_lines=new_sorted_lines, start_text=start_text)


@app.route('/map', methods=['POST', 'GET'])
def map_miigaik():
    return render_template('map.html')

#Регистрация для обычных пользователей(геоквест)
@app.route('/registration', methods=['POST', 'GET'])
def registration():

    if current_user.is_authenticated:
        print('12312')
        return redirect('/all_posts')

    if request.method == 'POST':
        login = request.form.get('login')
        name = request.form.get('name')
        surname = request.form.get('surname')
        thirdname = request.form.get('thirdname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password1')

        if login == '' or '@' not in login:
            flash('Неверно введена почта', 'danger')

        elif surname == '':
            flash('Введите Фамилию', 'danger')

        elif name == '':
            flash('Введите Имя', 'danger')

        elif thirdname == '':
            flash('Введите Отчество', 'danger')

        elif password1 == '':
            flash('Введите пароль', 'danger')

        elif password2 == '':
            flash('Введите пароль', 'danger')

        else:
            user = Users.query.filter_by(email=login).first()
            if user:
                flash('Пользователь уже существует', 'danger')
            else:
                if password1 == password2:
                    if len(password1) < 10:
                        flash('Длина пароля должна быть больше 10 символов', 'danger')
                    else:
                        try:
                            mailsend(login, password1)
                            password = generate_password_hash(password1)
                            user = Users(email=login, password=password, role='user', name=name, surname=surname,
                                         thirdname=thirdname)
                            db.session.add(user)
                            db.session.commit()
                            flash('Пользователь успешно зарегистрирован', 'success')
                            return redirect('/login')
                        except Exception as e:
                            flash('Неверно введена почта', 'danger')

    return render_template('/registration.html')

@app.route('/questions', methods=['POST', 'GET'])
def questions():
    is_exist_quest = GeoQuest.query.filter_by(id=1).all()
    for i in is_exist_quest:
        qsts = i.questions
        ans = i.answers
        qsts = qsts.split('^')
        ans = ans.split('^')

    if request.method == 'POST':
        quests = ''
        answers = ''
        for i in range(10):
            question = request.form.get(f'question{i}')
            answer = request.form.get(f'answer{i}')

            if question == '' or answer == '':
                flash('Не должно быть пустых ответов/вопросов', 'danger')
                return redirect('/questions')

            quests += f'{question}^'
            answers += f'{answer}^'

        if is_exist_quest:
            for i in is_exist_quest:
                i.questions = quests
                i.answers = answers
                db.session.commit()
        else:
            new_quest = GeoQuest(questions=quests, answers=answers)
            db.session.add(new_quest)
            db.session.commit()

        flash('Квест успешно создан!', 'success')
        return redirect('/questions')

    if not is_exist_quest:
        quest_for_output = GeoQuest(questions=[], answers=[])
        qsts = quest_for_output.questions
        ans = quest_for_output.answers
    print(ans)
    print(qsts)
    return render_template('questions.html', questions=qsts, answers=ans)

@app.route('/geoquest', methods=['POST', 'GET'])
def geoquest():
    if not current_user.is_authenticated:
        return redirect('/login')

    is_exist_quest = GeoQuest.query.filter_by(id=1).all()
    for i in is_exist_quest:
        quests = i.questions
        answers = i.answers

        quest = quests.split('^')
        quest.remove('')
        answers = answers.split('^')
        answers.remove('')

    current_user_progress = SaveGeoQuestProgress.query.filter_by(user=current_user.email).all()
    this_user_answers = []
    if not current_user_progress:
        this_user_answers = ['' for i in range(10)]
    for i in current_user_progress:
        this_user_answers.append(i.answer)
    print(this_user_answers)

    right_questions = []
    for i in range(len(answers)):
        if this_user_answers[i] == answers[i]:
            right_questions.append(i)

    if request.method == 'POST':
        for i in range(len(quest)):
            answer = request.form.get(f'answer{i}')
            this_user_check_answers = SaveGeoQuestProgress.query.filter_by(user=current_user.email, question_number=i).all()
            if not this_user_check_answers:
                new_answer = SaveGeoQuestProgress(user=current_user.email, question_number=i, answer=answer)
                db.session.add(new_answer)
            else:
                for i in this_user_check_answers:
                    i.answer = answer

        db.session.commit()
        return redirect('/geoquest')


    length = []
    for i in range(len(quest)):
        length.append(i)

    print(right_questions)
    return render_template('geoquest.html', questions=quest, length=length, right_questions=right_questions,
                           this_user_answers=this_user_answers)


@app.route('/post/<address>')
def post(address):
    post = Posts.query.filter_by(address=address).first()
    if post:
        text = post.text
        new_text = edit_text(text)
        count_images = id_counter(new_text, '#image#')
        count_videos = id_counter(new_text, '#video#')
        images_list = PostImages.query.filter_by(address=address).all()
        notes = get_notes(images_list)
        print(notes)
        videos_list = PostVideo.query.filter_by(address=address).all()
        if images_list:
            images_list = create_images_list(count_images, images_list)
        if videos_list:
            videos_list = create_videos_list(count_videos, videos_list)
        count = counter(new_text)
        images_list = image_editor(images_list)
        notes = put_notes(images_list, notes)
        print(notes)
        tags = PostTags.query.filter_by(address=address).all()
        tags_list = []
        for tag in tags:
            tags_list.append(tag.tag)
        for i in range(len(videos_list)):
            if videos_list[i] != '':
                videos_list[i] = videos_list[i].video_address
    else:
        return redirect('/')
    return render_template('post.html', post=post, new_text=new_text, notes=notes, images=images_list, count=count, tags=tags_list, videos_list=videos_list)


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
                        current_date = date()
                        left_date = '1779-01-01'
                        post = Posts(address=address, header=header, text=text, main_image=main_image, visible=visible, creation_time=current_date, left_date=left_date, right_date=current_date)
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
    current_date = date()
    tags = PostTags.query.filter_by(address=address).all()
    tags_list = []
    for tag in tags:
        tags_list.append(tag.tag)
    post = Posts.query.filter_by(address=address).first()
    text = post.text
    new_text = edit_text(text)
    count_images = id_counter(new_text, '#image#')
    count_videos = id_counter(new_text, '#video#')
    count = counter(new_text)
    left_date = post.left_date
    right_date = post.right_date
    if request.method == 'POST':
        notes = []
        images = []
        creator = request.form.get('creator')
        videos = []
        for i in count_videos:
            video = request.form.get(f'video{i}')
            videos.append(video)
        if videos:
            for video in videos:
                check = check_video(video)
                if check == False:
                    flash('Неверная ссылка на одном из видео', 'danger')
                    return redirect(f'/confirmpost/{address}')
            for video in videos:
                video_url = get_html(video)
                post_video = PostVideo(address=address, video_address=video_url)
                db.session.add(post_video)
                db.session.commit()
        for i in count_images:
            note = request.form.get(f'note{i}')
            if note == '':
                flash('Введите описания', 'danger')
                return redirect(f'/confirmpost/{address}')
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
        if len(count_images) == len(notes):
            if len(count_images) == len(images):
                upload_images(notes, images, address)
                post.visible = 'yes'
                post.creator = creator
                post.left_date = request.form.get('left-date')
                post.right_date = request.form.get('right-date')
                db.session.commit()
                return redirect(f'/generate_qr_code/{address}')
            else:
                flash('Добавьте картинки', 'danger')
        else:
            flash('Добавьте описания', 'danger')
    return render_template('confirm_post.html', post=post, new_text=new_text, count=count, tags=tags_list,
                           name=f'{current_user.surname} {current_user.name[0]}. {current_user.thirdname[0]}.',
                           current_date=current_date, left_date=left_date, right_date=right_date)

@app.route('/generate_qr_code/<address>', methods=['GET'])
@login_required
def generate_qr_code(address):
    img_base64 = qrcode_generate(address)
    return render_template('qr_code.html', qr_img_base64=img_base64, post_address=address)


@app.route('/print_qr_code_as_pdf/<address>')
@login_required
def print_qr_code_as_pdf(address):
    qr_code = QRCode.query.filter_by(post_id=address).first()
    if qr_code:
        img_base64 = qr_code.image_base64
        img_bytes = base64.b64decode(img_base64)
        try:
            pdf_buffer = BytesIO()
            c = canvas.Canvas(pdf_buffer, pagesize=letter)
            qr_img = ImageReader(BytesIO(img_bytes))
            c.drawImage(qr_img, 1.3 * inch, 2 * inch, width=6 * inch, height=6 * inch)
            img_path = current_app.root_path + '/static/qr_image/logo_qr.png'
            c.drawImage(img_path, 1.3 * inch, 8 * inch, width=6.2 * inch, height=2 * inch)
            c.save()
            pdf_buffer.seek(0)
            return send_file(pdf_buffer, mimetype='application/pdf', as_attachment=True, download_name='qr_code.pdf')
        except Exception as e:
            print(e)
            abort(500)
    else:
        abort(404)

@app.route('/show_qr_code/<address>')
@login_required
def show_qr_code(address):
    qr_code = QRCode.query.filter_by(post_id=address).first()
    if qr_code:
        qr_img_base64 = qr_code.image_base64
    else:
        qr_img_base64 = qrcode_generate(address)

    return render_template('qr_code.html', qr_img_base64=qr_img_base64, post_id=address)


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
    new_text = edit_text(post.text)
    main_image_in_post = post.main_image
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
            check_text = edit_text(text)
            if len(new_text) == len(check_text):
                post.text = text
            else:
                flash('Нельзя добавлять картинки и видео в уже существующий пост', 'danger')
                return redirect(f'/editpost/{address}')
        if header:
            post.header = header
        if error == False:
            db.session.commit()
            return redirect(f'/confirmedit/{address}')
        else:
            flash('Картинка не может быть такого типа', 'danger')
    return render_template('edit_post.html', post=post, tags=tags, titps=tags_in_this_post_list, image=main_image_in_post)


@app.route('/confirmedit/<address>', methods=['POST', 'GET'])
@login_required
def confirm_edit(address):
    current_date = date()
    tags = PostTags.query.filter_by(address=address).all()
    tags_list = []
    for tag in tags:
        tags_list.append(tag.tag)
    post = Posts.query.filter_by(address=address).first()
    left_date = post.left_date
    right_date = post.right_date
    text = post.text
    new_text = edit_text(text)
    count_images = id_counter(new_text, '#image#')
    count_videos = id_counter(new_text, '#video#')
    images_list = PostImages.query.filter_by(address=address).all()
    notes = get_notes(images_list)
    videos_list = PostVideo.query.filter_by(address=address).all()
    if images_list:
        images_list = create_images_list(count_images, images_list)
    if videos_list:
        videos_list = create_videos_list(count_videos, videos_list)
    count = counter(new_text)
    images_list = image_editor(images_list)
    notes = put_notes(images_list, notes)
    for i in range(len(videos_list)):
        if videos_list[i] != '':
            videos_list[i] = videos_list[i].video_address
    if request.method == 'POST':
        creator = request.form.get('creator')
        videos = []
        for i in count_videos:
            video = request.form.get(f'video{i}')
            videos.append(video)
        if videos:
            new_videos = []
            for video in videos:
                check = check_video(video)
                if check == False:
                    flash('Неверная ссылка на одном из видео', 'danger')
                    return redirect(f'/confirmpost/{address}')
            for video in videos:
                video_url = get_html(video)
                post_video = PostVideo(address=address, video_address=video_url)
                new_videos.append(post_video)
            old_videos = PostVideo.query.filter_by(address=address).all()
            for i in old_videos:
                db.session.delete(i)
                db.session.commit()
            for i in new_videos:
                db.session.add(i)
                db.session.commit()
        notes = []
        images = []
        for i in count_images:
            note = request.form.get(f'note{i}')
            if note == '':
                flash('Введите описания', 'danger')
                return redirect(f'/confirmpost/{address}')
            image = request.files[f'image{i}']
            if image:
                check = check_type_image(image)
                if check == False:
                    flash(f'Неподходящий тип картинки {i+1}', 'danger')
                else:
                    name = save_image(image, post.address, i)
                    images.append(name)
            else:
                images.append(images_list[i])
            if len(note) > 155:
                flash('Описание больше 155 символов', 'danger')
            else:
                notes.append(note)
        if len(count_images) == len(notes):
            if len(count_images) == len(images):
                images_in_this_post = PostImages.query.filter_by(address=address).all()
                for i in images_in_this_post:
                    db.session.delete(i)
                    db.session.commit()
                upload_images(notes, images, address)
                post.creator = creator
                post.left_date = request.form.get('left-date')
                post.right_date = request.form.get('right-date')
                db.session.commit()
                return redirect(f'/post/{address}')
            else:
                flash('Добавьте картинки', 'danger')
        else:
            flash('Добавьте описания', 'danger')
    return render_template('confirm_edit.html', post=post, new_text=new_text, count=count, tags=tags_list, current_date=current_date, left_date=left_date, right_date=right_date, notes=notes, images=images_list, videos_list=videos_list)


@app.route('/deletepost/<address>')
@login_required
def delete_post(address):
    post = Posts.query.filter_by(address=address).first()
    images_in_this_post = PostImages.query.filter_by(address=address).all()
    videos_in_this_post = PostVideo.query.filter_by(address=address).all()
    delete_images(images_in_this_post)
    delete_main(post)
    db.session.delete(post)
    for i in images_in_this_post:
        db.session.delete(i)
    for i in videos_in_this_post:
        db.session.delete(i)
    db.session.commit()
    return redirect('/allposts')


@app.route('/allposts', methods=['POST', 'GET'])
def all_posts():
    current_date = date()
    tags = Tags.query.all()
    tags_list = []
    filtered_posts = []
    post_list = []
    posts = Posts.query.order_by(desc(Posts.id)).all()
    if request.method == 'POST':
        type_of_sort = request.form.get('select')
        if type_of_sort == 'date':
            posts = Posts.query.order_by(desc(Posts.id)).all()
        else:
            posts = Posts.query.order_by(Posts.left_date).all()
        left_date = request.form.get('left-date')
        right_date = request.form.get('right-date')
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
            posts = filtered_posts
            posts = post_sort(posts, left_date, right_date)
            if type_of_sort == 'date':
                posts.reverse()
            return render_template('all_posts.html', posts=posts, tags=tags, current_date=current_date)
        else:
            posts = post_sort(posts, left_date, right_date)
            if tags_list:
                flash('Постов с таким наборов тегов нет', 'danger')
            return render_template('all_posts.html', posts=posts, tags=tags, current_date=current_date)
    return render_template('all_posts.html', posts=posts, tags=tags, current_date=current_date)


@manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)

def error(e):
    return render_template('error.html')


app.register_error_handler(404, error)
app.register_error_handler(401, error)


if __name__ == '__main__':
    db.create_all()
    posts = Posts.query.filter_by(visible='no')
    for post in posts:
        db.session.delete(post)
        db.session.commit()
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
