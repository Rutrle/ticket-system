from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///smart_ticket.db'
app.config['SECRET_KEY'] = '1292023cdb7b8e39f924afab'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from smart_ticket import routes