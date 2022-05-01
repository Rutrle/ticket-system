from sqlalchemy import ForeignKey, Column, Table
from smart_ticket import db, bcrypt
from smart_ticket import login_manager
from flask_login import UserMixin
from datetime import datetime
import secrets
import enum


current_solvers_association_table = Table('current_solvers_association', db.Model.metadata,
                                          Column('user_id', ForeignKey(
                                              'user.id'), primary_key=True),
                                          Column('ticket_id', ForeignKey(
                                              'ticket.id'), primary_key=True)
                                          )

ticket_watchlist_association_table = Table('ticket_watchlist_association', db.Model.metadata,
                                           Column('user_id', ForeignKey(
                                               'user.id'), primary_key=True),
                                           Column('ticket_id', ForeignKey(
                                               'ticket.id'), primary_key=True)
                                           )

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    creation_time = db.Column(
        db.DateTime(), nullable=False, default=datetime.now())
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email = db.Column(db.String(length=30), nullable=False, unique=True)
    phone_number = db.Column(db.String(length = 15), unique=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    profile_picture_file = db.Column(db.String(length = 64), default = "default_profile_picture.png")
    password_hash = db.Column(db.String(length=255),nullable=False, unique=True)
    password_salt = db.Column(db.String(length = 12))
    created_ticket_log_messages = db.relationship(
        'TicketLogMessage', backref='author', lazy=True)
    currently_solving = db.relationship(
        "Ticket", secondary=current_solvers_association_table,  back_populates="current_solvers")
    current_watchlist = db.relationship(
        "Ticket", secondary=ticket_watchlist_association_table,  back_populates="currently_on_watchlist")


    user_role_id = db.Column(db.Integer(),db.ForeignKey('userrole.id'))

    def __repr__(self) -> str:
        return f" User {self.username}"

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, plain_text_password):
        self.password_salt = secrets.token_hex(3)
        plain_text_password = self.password_salt + plain_text_password
        plain_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

        self.password_hash = plain_hash 

    def check_attempted_password(self, attempted_password):
        attempted_password = self.password_salt + attempted_password
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

class UserRole(db.Model):
    __tablename__ = 'userrole'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=64),nullable=False, unique=True)
    members = db.relationship('User', backref='user_role', lazy=True)

    def __repr__(self)-> str:
        return self.name


from functools import wraps
from flask_login import current_user
from flask import flash, redirect, url_for

def admin_required(function):

    @wraps(function)
    def wrap(*args, **kwargs):

        if current_user.user_role.name == "admin":
            return function(*args, **kwargs)
        else:
            flash("You need to be an admin to view this page.", category = 'danger')
            return redirect(url_for('home_page'))

    return wrap


class Ticket(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    subject = db.Column(db.String(length=45), nullable=False)
    issue_description = db.Column(db.Text(length=2500))
    creation_time = db.Column(
        db.DateTime(), nullable=False, default=datetime.now())
    author_id = db.Column(
        db.Integer(), db.ForeignKey('user.id'), nullable=True)
    author = db.relationship("User", foreign_keys=[author_id], backref = "created_tickets")

    current_solvers = db.relationship(
        "User", secondary=current_solvers_association_table, back_populates="currently_solving")
    currently_on_watchlist = db.relationship(
        "User", secondary=ticket_watchlist_association_table, back_populates="current_watchlist")

    is_solved = db.Column(db.Boolean(), nullable=False, default=False)
    solved_on = db.Column(db.DateTime(), nullable=True)

    solver_id = db.Column(
        db.Integer(), db.ForeignKey('user.id'), nullable=True)
    solver = db.relationship("User", foreign_keys=[solver_id], backref = "solved_tickets")

    log_messages = db.relationship(
        'TicketLogMessage', backref='ticket', lazy=True, cascade = 'all, delete')

    def __repr__(self) -> str:
        return f" Ticket No. {self.id} : {self.subject}"

    def solve_ticket(self, solver, solution_text):
        self.solver_id = solver.id
        self.is_solved = True
        self.solved_on = datetime.now()
        self.current_solvers = []
        
        solution_message = TicketLogMessage(
            author_id=solver.id, ticket_id=self.id, message_text=solution_text, message_category="solved")

        db.session.add(solution_message)
        db.session.add(self)
        db.session.commit()


class TicketogMessageCategory(enum.Enum):
    update = 'Update'
    solved = 'TICKET SOLVED'
    sys_message = 'System message'
    reopened = 'TICKET REOPENED'


class TicketLogMessage(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    author_id = db.Column(
        db.Integer(), db.ForeignKey('user.id'), nullable=True)
    ticket_id = db.Column(db.Integer(), db.ForeignKey(
        'ticket.id'), nullable=False)
    creation_time = db.Column(
        db.DateTime(), nullable=False, default=datetime.now())

    message_text = db.Column(db.Text(length=1500))
    message_category = db.Column(db.Enum(TicketogMessageCategory),nullable=False)

    def __repr__(self) -> str:
        return f" Ticket log message {self.id}, for ticket {self.ticket.subject}"

