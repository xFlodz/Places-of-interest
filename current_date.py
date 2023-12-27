import datetime


def date():
    current_date = datetime.datetime.now().date().strftime('%Y-%m-%d')
    return current_date
