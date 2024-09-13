import mailtrap as mt
import pathlib
from dotenv import load_dotenv
import os

load_dotenv(pathlib.Path(__file__).parent / ".env")

def send_email(text:str, recipient:str, subject:str, category:str):

    mail = mt.Mail(
        sender=mt.Address(email="no-reply@uacs.ca", name="UACS-No Reply"),
        to=[mt.Address(email=recipient), mt.Address(email="execs@uacs.ca")],
        subject=subject,
        text=text,
        category=category,
    )
    client = mt.MailtrapClient(token=os.getenv("MAILTRAP_TOKEN"))
    client.send(mail)
