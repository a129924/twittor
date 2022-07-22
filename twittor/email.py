from threading import Thread
import os

from flask import current_app
from flask_mail import Message
from twittor.mail_ext import mail


def send_async_email(app, message):
    with app.app_context():
        mail.send(message)

def send_email(subject, recipients, text_body, html_body):
    message = Message()
    
    message.subject = subject 
    message.recipients = recipients
    message.reply_to = "noreply@twittor.com"
    message.body = text_body
    message.html = html_body
    
    # mail.send(message)
    Thread(target=send_async_email,
           args=(current_app._get_current_object(), message)).start()
