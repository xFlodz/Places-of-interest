import os
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

def allowed_file(file, address):
    if '.' in file.filename and (file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS):
        print('1')
        address = 'static\post_images/' + address + "." + file.filename.rsplit('.', 1)[1].lower()
        file.save(address)
        check = 1
    else:
        check = 0
    return check


