from smart_ticket import db
from datetime import datetime, timedelta
from smart_ticket.models import User, Ticket, TicketLogMessage, UserRole
from faker import Faker
from random import randint
from sqlalchemy import func

""" 
script for deleting and recreating the database and filling it in with some data

database reset needs to be done before running SmartTicket application

rest of functions only fill database with dummy data and so their running is optional
"""


def database_reset() -> None:
    """
    deleting whole database and then creating it anew according to SmartTicket models,
    then it creates basic user roles and first admin (which should be used to upgrade custom user to administrator and then deleted)
    """
    db.drop_all()
    db.create_all()

    user_roles = []
    user_roles.append(UserRole(name="user"))
    user_roles.append(UserRole(name="admin"))

    for user_role in user_roles:
        db.session.add(user_role)
    db.session.commit()

    admin = User(username='admin', email='admin@mail.com', password='admin',
                 user_role=db.session.query(UserRole).filter_by(name="admin").first())

    db.session.add(admin)
    db.session.commit()


def create_dummy_tickets(ticket_num: int = 50) -> None:
    """
    fill the database with 'ticket_num' amount od random ticket (dummy data)
    only for testing/showing
    """
    fake = Faker()
    tickets = []
    max_user_id = db.session.query(func.max(User.id)).scalar()

    for i in range(ticket_num):
        tickets.append(Ticket(subject=fake.unique.sentence(), issue_description=fake.text(), creation_time=(
            datetime.now() - timedelta(days=randint(0, 180))), author_id=randint(1, max_user_id)))

    for ticket in tickets:
        db.session.add(ticket)
    db.session.commit()

    ticket_creation_logs = []

    for ticket in tickets:
        ticket_creation_logs.append(TicketLogMessage(
            ticket_id=ticket.id, message_text="Ticket opened", message_category="sys_message"))

    for ticket_log in ticket_creation_logs:
        db.session.add(ticket_log)

    db.session.commit()


def create_solved_dummy_tickets(ticket_num: int = 50) -> None:
    """
    fill the database with 'ticket_num' amount od random solved ticket (dummy data)
    only for testing/showing
    """
    fake = Faker()
    tickets = []
    max_user_id = db.session.query(func.max(User.id)).scalar()

    for i in range(ticket_num):
        tickets.append(Ticket(subject=fake.unique.sentence(), issue_description=fake.text(), creation_time=(datetime.now() - timedelta(days=randint(180, 360))),
                       author_id=randint(1, max_user_id), solved_on=(datetime.now() - timedelta(days=randint(0, 180))), solver_id=randint(1, max_user_id), is_solved=True))

    for ticket in tickets:
        db.session.add(ticket)
    db.session.commit()

    ticket_creation_logs = []

    for ticket in tickets:
        ticket_creation_logs.append(TicketLogMessage(
            ticket_id=ticket.id, message_text="Ticket opened", message_category="sys_message"))
        ticket_creation_logs.append(TicketLogMessage(ticket_id=ticket.id, message_text=fake.text(
        ), message_category="solved", author_id=ticket.solver_id))

    for ticket_log in ticket_creation_logs:
        db.session.add(ticket_log)

    db.session.commit()


def create_dummy_users(users_num: int = 50, locale: str = "DE") -> None:
    """
    fills in database with 'user_num' amount of random dummy user profiles from 'locale' localization
    only for testing/showing
    """
    fake = Faker(
        locale=locale)  # locale is used to prevent phone number extensions to be generated in phone numbers
    users = []

    for i in range(users_num):
        users.append(User(username=fake.unique.name(), email=fake.unique.free_email(), password=fake.password(),
                          phone_number=fake.phone_number(), user_role=db.session.query(UserRole).filter_by(name="user").first()))

    for user in users:
        db.session.add(user)
    db.session.commit()


def fill_in_database() -> None:
    """
    fill the database with defined dummy data so the functionality of SmartTicket can be seen/tested
    only for testing/showing
    """
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

    users = []
    tickets = []
    ticket_creation_logs = []

    users.append(User(username='User1', email='user1@mail.com', password='password',
                 phone_number='+420123456789', user_role=db.session.query(UserRole).filter_by(name="user").first()))
    users.append(User(username='Greorge Sharp', email='user2@mail.com', password='password2',
                 phone_number='+420993456789', user_role=db.session.query(UserRole).filter_by(name="user").first()))
    users.append(User(username='User3', email='user3@mail.com', password='password3',
                 phone_number='+420123444789', user_role=db.session.query(UserRole).filter_by(name="user").first()))
    users.append(User(username='Josef Smith', email='smith3@mail.com', password='password',
                 user_role=db.session.query(UserRole).filter_by(name="user").first()))
    users.append(User(username='ExEmployee', email='exemployee@mail.com', password='123456',
                 is_active=False, user_role=db.session.query(UserRole).filter_by(name="user").first()))
    users.append(User(username='ExEmployee2', email='exemployee2@mail.com', password='123456',
                 is_active=False, user_role=db.session.query(UserRole).filter_by(name="user").first()))
    users.append(User(username='ExEmployee3', email='exemployee3@mail.com', password='123456',
                 is_active=False, user_role=db.session.query(UserRole).filter_by(name="user").first()))
    users.append(User(username='ExEmployee4', email='exemployee4@mail.com', password='123456',
                 is_active=False, user_role=db.session.query(UserRole).filter_by(name="user").first()))
    users.append(User(username='ExEmployee5', email='exemployee5@mail.com', password='123456',
                 is_active=False, user_role=db.session.query(UserRole).filter_by(name="user").first()))
    for user in users:
        db.session.add(user)
    db.session.commit()

    u = User.query.filter_by(username='User3').first()
    u1 = User.query.filter_by(username='User1').first()
    u2 = User.query.filter_by(username='Greorge Sharp').first()

    tickets.append(Ticket(subject='Something broke',
                   issue_description="something has broken, it's not my fault"))
    tickets.append(Ticket(subject='Something else broke',
                   issue_description=long_text))
    tickets.append(Ticket(subject='Lorem ipsum',
                   issue_description=longer_text))
    tickets.append(Ticket(subject='Owned ticket',
                   issue_description="I was created by user3", author_id=u.id))
    tickets.append(Ticket(subject='Coffee is cold',
                   issue_description="Coffee machine on floor 3 makes coffee too cold", author_id=u1.id))
    tickets.append(Ticket(subject='Solved ticket', issue_description="I was solved by user3",
                   solved_on=datetime.now(), author_id=u.id, solver_id=u.id, is_solved=True))
    tickets.append(Ticket(subject='Keyboard not working', issue_description="Keyboard is not working",
                   solved_on=datetime.now() - timedelta(days=3), author_id=u.id, solver_id=u2.id, is_solved=True))
    tickets.append(Ticket(subject='Solved ticket', issue_description="I was solved by user2",
                   solved_on=datetime.now() - timedelta(days=5), solver_id=u2.id, is_solved=True))
    tickets.append(Ticket(subject='Browser not functioning properly', issue_description="I was solved by user2",
                   solved_on=datetime.now() - timedelta(days=5), solver_id=u1.id, is_solved=True))
    tickets.append(Ticket(subject='Room is too dark',
                   issue_description="Room that I'm sitting in has too many broken lightbulbs so it's dark in it"))
    tickets.append(Ticket(subject='Room is too brigh',
                   issue_description="Room that I'm sitting in has too many lightbulbs so it's too bright in it"))
    tickets.append(Ticket(subject='Too many bugs',
                   issue_description="There are too many bugs in program XYZ"))
    tickets.append(Ticket(subject='Coffee is hot',
                   issue_description="Coffee machine on floor 2 makes coffee too hot", author_id=u1.id))

    for ticket in tickets:
        db.session.add(ticket)

    db.session.commit()

    for ticket in tickets:
        ticket_creation_logs.append(TicketLogMessage(
            ticket_id=ticket.id, message_text="Ticket opened", message_category="sys_message"))

    for ticket_log in ticket_creation_logs:
        db.session.add(ticket_log)

    db.session.commit()


if __name__ == "__main__":
    database_reset()
    fill_in_database()

    create_dummy_users(10, "CZ")
    create_dummy_users(10, "DE")
    create_dummy_users(10, "en_GB")
    create_dummy_users(10, "en_US")
    create_dummy_users(10, "fr_FR")
    create_solved_dummy_tickets()
    create_dummy_tickets()