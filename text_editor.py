import re

def text_editor(text):
    text = text.split('$')
    return text

def get_notes(image_list):
    notes = []
    for i in image_list:
        notes.append(i.note)
    return notes
