from smart_ticket import db, bcrypt


class User(db.Model):
    id = db.Column(db.Integer(),primary_key = True)
    creation_time = db.Column(db.DateTime(),nullable=False)
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

class Ticket(db.Model):
    id = db.Column(db.Integer(),primary_key = True)
    subject = db.Column(db.String(length=30), nullable=False)
    issue_description = db.Column(db.Text(length=2500))
    creation_time = db.Column(db.DateTime(),nullable=False)
    author_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=True)
    is_solved = db.Column(db.Boolean(), nullable=False)

    def __repr__(self) -> str:
        return f" Ticket No. {self.id}, : {self.subject}"