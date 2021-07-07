from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from starlette.requests import Request
from settings.settings import EMAIL_HOST, EMAIL_HOST_PASSWORD, EMAIL_PORT, EMAIL_HOST_USER
from user.schemas import UserDB


def send_email(
        *,
        message: str,
        to_address: str,
        subscription: str,
        password: str = EMAIL_HOST_PASSWORD,
        from_address: str = EMAIL_HOST_USER,

):
    # setup the parameters of the message
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subscription

    # add in the message body
    msg.attach(MIMEText(message, 'plain'))

    # create server
    server = smtplib.SMTP(host=EMAIL_HOST, port=EMAIL_PORT)

    server.starttls()

    # Login Credentials for sending the mail
    server.login(msg['From'], password)

    # send the message via the server.
    server.sendmail(msg['From'], msg['To'], msg.as_string())

    server.quit()
