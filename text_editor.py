import re

def text_editor(text):

    notes = re.findall(r'\{(.*?)\}', text)
    text_without_braces = re.sub(r'\{(.*?)\}', ' ', text)
    text_list = text_without_braces.split()

    mini_text = []
    for i in text_list:
        if '/' in i:
            i = i.replace('/', '')
            mini_text.append(i)
    return mini_text, notes
