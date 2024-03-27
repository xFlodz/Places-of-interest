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
        if 'embed' in address:
            new_address = address.split('&')
            new_address = new_address[0].replace('https://www.youtube.com/embed/', '')
        else:
            new_address = address.split('&')
            new_address = new_address[0].replace('https://www.youtube.com/watch?v=', '')
    return new_address






