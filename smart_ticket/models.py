from sqlalchemy import ForeignKey, Column, Table
from smart_ticket import db, bcrypt
from smart_ticket import login_manager
from flask_login import UserMixin
from datetime import datetime


current_solvers_association_table = Table('current_solvers_association',db.Model.metadata,
    Column('user_id',ForeignKey('user.id'), primary_key = True),
    Column('ticket_id',ForeignKey('ticket.id'), primary_key = True)
)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(),primary_key = True)
    creation_time = db.Column(db.DateTime(),nullable=False, default = datetime.now())
    username = db.Column(db.String(length = 30), nullable=False, unique = True)
    email = db.Column(db.String(length = 30), nullable=False, unique = True)
    password_hash = db.Column(db.String(length = 50), nullable=False, unique = True)
    #created_tickets = db.relationship('Ticket', back_populates='author', lazy=True)
    #solved_tickets = db.relationship('Ticket', back_populates='solver', lazy=True)
    created_ticket_log_messages = db.relationship('TicketLogMessage',backref='author', lazy=True)
    currently_solving = db.relationship("Ticket",secondary = current_solvers_association_table,  back_populates = "current_solvers" )

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
    subject = db.Column(db.String(length=45), nullable=False)
    issue_description = db.Column(db.Text(length=2500))
    creation_time = db.Column(db.DateTime(),nullable=False, default = datetime.now())

    author_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=True)
    author = db.relationship("User", foreign_keys =[author_id])

    solver_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=True)
    solver =  db.relationship("User", foreign_keys =[solver_id])

    current_solvers = db.relationship("User", secondary = current_solvers_association_table, back_populates = "currently_solving" )

    is_solved = db.Column(db.Boolean(), nullable=False, default = False)
    log_messages = db.relationship('TicketLogMessage',backref='ticket', lazy=True)

    def __repr__(self) -> str:
        return f" Ticket No. {self.id} : {self.subject}"
    


class TicketLogMessage(db.Model):
    id = db.Column(db.Integer(),primary_key = True)
    author_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=True)
    creation_time = db.Column(db.DateTime(),nullable=False, default = datetime.now())
    ticket_id = db.Column(db.Integer(), db.ForeignKey('ticket.id'), nullable=False)
    message_text = db.Column(db.Text(length=1500))
    
    def __repr__(self) -> str:
        return f" Ticket log message {self.id}, for ticket {self.ticket.subject}"