def check_video(address):
    if ('youtube' in address) or ('youtu.be' in address):
        return True
    else:
        return False


def get_html(address):
    if 'youtu.be' in address:
        new_address = address.split('?')
        new_address = new_address[0].replace('https://youtu.be/', '')
    if 'youtube' in address:
        new_address = address.split('&')
        new_address = new_address[0].replace('https://www.youtube.com/watch?v=', '')
        new_address = new_address[0].replace('https://www.youtube.com/embed/', '')
    return new_address






