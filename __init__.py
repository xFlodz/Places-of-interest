from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

app = Flask(__name__)
app.app_context().push()
app.secret_key = 'ABC123'
app.config['FLASK_ENV'] = 'development'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['ROLES'] = ['admin', 'poster']

db = SQLAlchemy(app)
manager = LoginManager(app)

migrate = Migrate(app, db)