def counter(text):
    a = []
    count = len(text)
    for i in range(count):
        a.append(i)
    return a


def id_counter(text, check):
    new_list = []
    for i in range(len(text)):
        if check == text[i]:
            new_list.append(i)
    return new_list
