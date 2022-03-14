from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from smart_ticket.auth.routes import auth_blueprint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///smart_ticket.db'
app.config['SECRET_KEY'] = '1292023cdb7b8e39f924afab'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)



login_manager = LoginManager(app)
app.register_blueprint(auth_blueprint, url_prefix = '/auth')
from smart_ticket import routes, filters

