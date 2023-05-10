import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase

from  models import *

from email import encoders

SMTP_SERVER_HOST="localhost"
SMTP_SERVER_PORT=1025
SENDER_ADDRESS="kanban.app.v2@MAD2.com"
SENDER_PASSWORD="nymphadora"


def send_email(receivers, subject, message, attachment):
    msg=MIMEMultipart()
    msg['From'] = SENDER_ADDRESS
    msg['To'] = receivers
    msg['Subject']  = subject

    msg.attach(MIMEText(message, "html"))

    with open(attachment, "rb") as pdf:
        part=MIMEBase("application","octate-stream", Name="your_report.pdf")
    
        part.set_payload(pdf.read())

    encoders.encode_base64(part)

    part.add_header('Content-Disposition', 'attachment', filename=attachment)

    msg.attach(part)

    s=smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)
    s.login(SENDER_ADDRESS,SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()
    return True





