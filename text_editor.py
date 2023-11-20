import re

def text_editor(text):
    text = text.split('$')
    return text

def get_notes(image_list, address):
    image_list = image_list.split(' ')
    image_list.pop()
    notes = []
    for i in range(len(image_list)):
        image_list[i] = image_list[i].replace(address,' ')
        image_list[i] = image_list[i].replace(f'static/post_images/{i}', '')
        image_list[i].split(' ')
        note = image_list[i].split(' ')
        notes.append(note[0])
    return notes

