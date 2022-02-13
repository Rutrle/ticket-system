from email.policy import default
from smart_ticket import db, bcrypt
from smart_ticket import login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(),primary_key = True)
    creation_time = db.Column(db.DateTime(),nullable=False, default = datetime.now())
    username = db.Column(db.String(length = 30), nullable=False, unique = True)
    email = db.Column(db.String(length = 30), nullable=False, unique = True)
    password_hash = db.Column(db.String(length = 30), nullable=False, unique = True)
    created_tickets = db.relationship('Ticket',backref='author', lazy=True)

    def __repr__(self) -> str:
        return f" User {self.username}"

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, plain_text_password):
        self.password_hash= bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_attempted_password(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


class Ticket(db.Model):
    id = db.Column(db.Integer(),primary_key = True)
    subject = db.Column(db.String(length=30), nullable=False)
    issue_description = db.Column(db.Text(length=2500))
    creation_time = db.Column(db.DateTime(),nullable=False, default = datetime.now())
    author_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=True)
    is_solved = db.Column(db.Boolean(), nullable=False)

    def __repr__(self) -> str:
        return f" Ticket No. {self.id}, : {self.subject}"