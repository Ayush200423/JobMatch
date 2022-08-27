from email.message import EmailMessage
import ssl
import smtplib
import random

from mail_config import email_sender, email_password

class Mailer:
    def __init__(self):
        self.email_sender = email_sender
        self.email_password = email_password

    def setup_email(self, user_email):
        code = random.randint(100000, 999999)
        self.email_receiver = user_email
        subject = "Thank you for using JobMatch!"
        body = f'''
        This is an automated email, please do not reply to it.

        If you have any questions or concerns, feel free to contact me on my LinkedIn.

        LinkedIn: https://www.linkedin.com/in/ayush2004/

        If you did not sign up to JobMatch, please ignore this email.
        '''
        self.em = EmailMessage()
        self.em['From'] = email_sender
        self.em['To'] = self.email_receiver
        self.em['subject'] = subject
        self.em.set_content(body)

    def send_email(self):
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(self.email_sender, self.email_receiver, self.em.as_string())