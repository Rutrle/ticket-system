from re import T
from smart_ticket import db
from datetime import datetime
from smart_ticket.models import  User, Ticket, TicketLogMessage

'''
script for deleting and recreating the database and filling it in with some data

also used for trying out database communication during development - these parts will be deleted later
'''


db.drop_all()
db.create_all()

long_text = "Est eiusmod sunt in velit cillum enim consectetur pariatur ullamco. Quis pariatur anim deserunt irure voluptate aute reprehenderit enim minim aliquip laboris et. Nostrud consectetur ex non ullamco Lorem commodo. Cillum magna dolore occaecat duis laborum consequat. Duis Lorem reprehenderit ex dolore elit excepteur in qui cupidatat in reprehenderit. Id eu minim elit mollit. Occaecat ea ipsum do ullamco laborum nostrud ipsum Lorem ullamco elit."
longer_text = """Ullamco deserunt deserunt officia ad nisi consequat adipisicing velit cupidatat nulla qui enim magna. Esse sint esse proident enim elit dolor amet. Velit culpa amet enim dolore est.
            Excepteur sint reprehenderit cillum proident fugiat duis nulla pariatur consequat. Adipisicing duis incididunt tempor consequat incididunt Lorem. Fugiat ea sint aliqua reprehenderit cupidatat laboris culpa nostrud veniam laboris sit pariatur do ut. Enim consectetur qui ut eiusmod eiusmod in. Incididunt adipisicing magna proident pariatur nostrud nisi quis veniam sunt magna eu id. Magna ad aliquip voluptate sunt mollit id Lorem magna. Nisi amet magna elit dolor ea mollit laboris aliquip ullamco ipsum nisi.
            Occaecat in aliqua officia sit consectetur et quis enim consequat culpa labore in ea in. Proident laboris est aliquip quis non est minim qui eiusmod quis. Id cupidatat id officia aliqua duis adipisicing ipsum cupidatat anim consequat. Aute voluptate dolor ut cupidatat velit ea sit cupidatat laboris id minim reprehenderit dolor incididunt.
            Aute incididunt cillum aliqua duis qui nulla laboris consectetur esse labore sit incididunt. Et incididunt anim cupidatat voluptate velit culpa irure proident culpa enim. Sint laboris sint laborum sint labore labore qui sint pariatur culpa occaecat. In qui non et adipisicing irure irure amet qui laborum ea ea elit eiusmod qui. Sit occaecat magna consectetur culpa et Lorem commodo ipsum ullamco non. Tempor sunt in fugiat tempor nostrud ea.
            Voluptate veniam minim nisi ex est officia nostrud duis et nostrud. Nisi dolore sunt eiusmod aliquip qui ullamco. Elit ex eu nulla tempor ad tempor velit.
            Reprehenderit officia eiusmod voluptate reprehenderit dolore nulla incididunt. Lorem commodo exercitation tempor id officia ipsum velit aliquip ut exercitation. Enim mollit culpa mollit tempor. Dolor esse ea elit excepteur qui Lorem sit enim ullamco id.
            Officia proident do labore consequat aliqua reprehenderit amet aliqua. Do tempor consectetur dolore tempor consequat voluptate nostrud magna ad irure culpa sit laborum incididunt. Laborum dolore dolore ipsum mollit sit pariatur aute eiusmod cupidatat. Fugiat dolore laborum commodo et duis culpa eu in nostrud. Elit reprehenderit nulla aute sunt tempor commodo pariatur cupidatat duis et sunt exercitation. In dolore pariatur ad sint proident.
            Ipsum culpa Lorem cillum dolore et ea duis adipisicing mollit. Dolor laboris qui nostrud mollit excepteur occaecat ad dolor. Sint labore do deserunt esse ad non minim non exercitation magna veniam aute. Proident dolore exercitation id mollit anim eu exercitation aliqua. Fugiat laborum velit ipsum exercitation incididunt. Occaecat fugiat occaecat deserunt in minim cupidatat culpa cupidatat qui irure. Laboris ipsum consectetur aute quis proident dolor aliquip ea occaecat pariatur officia.
            """
users=[]
tickets=[]
ticket_creation_logs=[]

users.append(User(username='User1', email='user1@mail.com',password='password'))
users.append(User(username='User2', email='user2@mail.com',password='password2'))
users.append(User(username='User3', email='user3@mail.com',password='password3'))
users.append(User(username='Josef Smith', email='smith3@mail.com',password='password'))
for user in users:
    db.session.add(user)
db.session.commit()

u=User.query.filter_by(username='User3').first()
print(u)

tickets.append(Ticket(subject='Something broke',issue_description = "something has broken, it's not my fault"))
tickets.append(Ticket(subject='Something else broke',issue_description = long_text))
tickets.append(Ticket(subject='Lorem ipsum',issue_description = longer_text))
tickets.append(Ticket(subject='Owned ticket',issue_description = "I belong to user3",author_id =u.id ))
tickets.append(Ticket(subject='Solved ticket',issue_description = "I was solved by user3", solved_on = datetime.now(),author_id =u.id, solver_id = u.id, is_solved=True ))

for ticket in tickets:
    db.session.add(ticket)

db.session.commit()

for ticket in tickets:
    ticket_creation_logs.append(TicketLogMessage(ticket_id=ticket.id, message_text = "Ticket opened"))

for ticket_log in ticket_creation_logs:
    db.session.add(ticket_log)

db.session.commit()


t = Ticket.query.filter_by(subject='Owned ticket').first()
print(t)
print(t.author)
print(t.creation_time)
