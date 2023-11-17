import re

def text_editor(text):
    inside_brackets = re.findall(r'{(.*?)}', text)
    outside_brackets = re.split(r'{.*?}', text)

    inside_brackets = [item.strip() for item in inside_brackets if item.strip()]
    outside_brackets = [item.strip() for item in outside_brackets if item.strip()]

    return outside_brackets, inside_brackets