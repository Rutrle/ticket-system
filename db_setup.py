from smart_ticket import db
from datetime import datetime
from smart_ticket.models import  User, Ticket

'''
script for deleting and recreating the database and filling it in with some data
'''




db.drop_all()
db.create_all()



user1 = User(username='User1',creation_time =datetime.now(), email='user1@mail.com',password_hash='password')
ticket1 = Ticket(subject='Something broke',issue_description = "something has broken, it's not my fault",creation_time =datetime.now(),is_solved=False)

db.session.add(user1, ticket1)


db.session.commit()