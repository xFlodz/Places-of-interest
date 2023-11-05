from flask import render_template, flash
from models import Users, Posts

from __init__ import db, app, manager


@app.route('/')
def index():
    return render_template('index.html')


@manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


if __name__ == '__main__':
    #db.create_all()
    app.run(host='0.0.0.0',port=8080,debug=True)
