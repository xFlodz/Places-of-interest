import random
from models import Posts


def create_address():
    address = ''
    for x in range(16):
        address = address + random.choice(list('1234567890abcdefghigklmnopqrstuvyxwzABCDEFGHIGKLMNOPQRSTUVYXWZ'))
    address_check = Posts.query.filter_by(address=address).first()
    if address_check:
        create_address()
    else:
        return address


