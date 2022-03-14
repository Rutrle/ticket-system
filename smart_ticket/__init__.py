from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///smart_ticket.db'
app.config['SECRET_KEY'] = '1292023cdb7b8e39f924afab'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


login_manager = LoginManager(app)

from smart_ticket.user.routes import user_blueprint
app.register_blueprint(user_blueprint, url_prefix = '/user')

from smart_ticket import routes, filters

