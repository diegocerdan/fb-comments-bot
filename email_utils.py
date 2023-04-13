import smtplib, ssl
from decouple import config

SMTP_PORT = 587
SMTP_SERVER = config('SMTP_SERVER')
SENDER_EMAIL = config('SENDER_EMAIL')
PASSWORD_EMAIL = config('PASSWORD_EMAIL')

def send_email(receiver_email, subject, content):
    message = 'Subject: ' + subject + '\n\n' + content
    context = ssl.create_default_context()
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls(context=context)
        server.login(SENDER_EMAIL, PASSWORD_EMAIL)
        server.sendmail(SENDER_EMAIL, receiver_email, message)