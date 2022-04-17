from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_ckeditor import CKEditor


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///smart_ticket.db'
app.config['SECRET_KEY'] = '1292023cdb7b8e39f924afab'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
ckeditor = CKEditor(app)

login_manager = LoginManager(app)

from smart_ticket.user_bp.routes import user_bp
from smart_ticket.ticket_bp.routes import ticket_bp
from smart_ticket.admin_bp.routes import admin_bp

app.register_blueprint(user_bp, url_prefix = '/user')
app.register_blueprint(ticket_bp, url_prefix = '/ticket')
app.register_blueprint(admin_bp, url_prefix = '/admin')

from smart_ticket import routes, filters

