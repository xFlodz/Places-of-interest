import os
ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png']


def check_type_main(main):
    file = main
    check = True
    if '.' in file.filename and (file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS):
        return check
    else:
        check = False
        return check

def check_type_images(images):
    check = True
    for file in images:
        if '.' in file.filename and (file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS):
            pass
        else:
            check = False
            return check
    return check


def save_images(files, address):
    names = ''
    count = 1
    for file in files:
        name = 'static/post_images/' + address + str(count) + '.' + file.filename.rsplit('.', 1)[1].lower()
        file.save(name)
        names = names + name + ' '
        count += 1
    return  names


def save_main(file, address):
    name = 'static/main_images/' + address + "." + file.filename.rsplit('.', 1)[1].lower()
    file.save(name)
    return name

