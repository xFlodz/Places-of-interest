import os
from models import PostImages
from __init__ import db
ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png']


def check_type_image(file):
    check = True
    if '.' in file.filename and (file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS):
        return check
    else:
        check = False
        return check




def save_image(file, address, i):
    name = 'static/post_images/' + str(i) + address + "." + file.filename.rsplit('.', 1)[1].lower()
    file.save(name)
    return name


def save_main(file, address):
    name = 'static/main_images/' + address + "." + file.filename.rsplit('.', 1)[1].lower()
    file.save(name)
    return name

def upload_images(notes, images_list, address):
    names = ''
    for i in range(len(images_list)):
        file_name = images_list[i]
        note = notes[i]
        image = PostImages(address=address, note=note, path_to_image=file_name)
        db.session.add(image)
        db.session.commit()

