import re
def get_notes(image_list):
    notes = []
    for i in image_list:
        notes.append(i.note)
    return notes

def put_notes(images_list, old_notes):
    n = 0
    new_list = images_list.copy()
    for i in range(len(new_list)):
        if new_list[i] != '':
            new_list[i] = old_notes[n]
            n+=1
    return new_list


def edit_text(text):
    new_text = text.replace('$', '$#image#$')
    new_text = new_text.replace('&', '$#video#$')
    new_text = new_text.split('$')
    while '' in new_text:
        new_text.remove('')
    return new_text
