import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from smart_ticket.settings import EMAIL_PASSWORD
from flask import url_for

PORT = 465  # For SSL
SMTP_SERVER = "smtp.gmail.com"
SENDER_EMAIL = "smartticketbot@gmail.com"  # Enter your address


def send_email(receiver_email:str, subject:str, email_text:str, email_html:str):

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = SENDER_EMAIL
    message["To"] = receiver_email

    part1 = MIMEText(email_text, "plain")
    part2 = MIMEText(email_html, "html")

    message.attach(part1)
    message.attach(part2)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, PORT, context=context) as server:
        server.login(SENDER_EMAIL, EMAIL_PASSWORD)
        server.sendmail(SENDER_EMAIL, receiver_email, message.as_string())


def send_registration_email(receiver_email:str, username:str):
    subject = "Welcome to Smart ticket"

    email_text =  f"""Welcome to Smart Ticket, {username}!
                To Log in please use the following link: {url_for('user_bp.login_page', _external = True)}'
                We hope You will have great time using our app
    
                If You have not created account on SmartTicket, please ignore this e-mail
                
                Yours sincerely
                Smart Ticket development team
                
                """

    email_html = f"""<h1>Welcome to Smart Ticket!, {username}</h1>
                <hr>
                <p>To Log in please use the following <a href='{url_for('user_bp.login_page', _external = True)}'>link</a></p>
                <p>We hope You will have great time using our app</p>
                <br>
                <p>If You have not created account on SmartTicket, please ignore this e-mail</p>
                <br>
                <br>
                <p>Yours sincerely</p>
                <br>
                <p>Smart Ticket development team</p>
                """
    
    
    send_email(receiver_email, subject, email_text, email_html)


def send_deactivation_email(receiver_email:str, username:str):
    subject = "Smart ticket account deactivation"

    email_text = f"""
                Your Smart Ticket account, {username}, was deactivated
                You will no longer be able to log in to Smart Ticket and use most of its features

                If you have any questions regarding the deactivation, please contact your administrator

                Yours sincerely

                Smart Ticket development team
                """ 

    email_html = f"""<h1>Your Smart Ticket account, {username}, was deactivated</h1>
                <hr>
                <p>You will no longer be able to log in to Smart Ticket and use most of its features</p>
                <p>If you have any questions regarding the deactivation, please contact your administrator</p>
                <br>
                <br>
                <p>Yours sincerely</p>
                <br>
                <p>Smart Ticket development team</p>
                """
    
    
    send_email(receiver_email, subject, email_text, email_html)