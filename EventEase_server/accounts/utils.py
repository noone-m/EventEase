from random import randint
from django.conf import settings
from django.core.mail import send_mail
from twilio.rest import Client
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import secrets
import smtplib
import os


load_dotenv()


def random_code():
    """
    Generate random code of sex numbers.
 
    Returns
    -------
    code(str) : the genertated random code
    """

    code = ""
    for i in range(6):
        num = randint(0,9)
        code += f"{num}"
    return code


def send_message(method,sender_number,recipient_number,msg):
    """
    send messages to provided number.
    
    diffrent methods to send the message:

    + 'twilio' : send sms messages using twilio provider.

    + 'pywhatkit' : send whatsapp messages using pywhatkit package this method is not good at all and you can never 
    it in production environment.But I was forced to use it in test because of sanction in syria.
    you can still use it in testing but I don't recommend.In production you can use the official whatsapp buisness 
    API.

    parametrs
    ---------
    method(str): the method to send messages.

    sender_number(str): the phone number of the sender

    recipient_number(str): the phone number of the recipient

    msg(str): the message you want to sent
    """

    if method == 'twilio':
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=msg,
            from_=sender_number,
            to= recipient_number
        )
        
    if method == 'pywhatkit':
        pass
        #pywhatkit.sendwhatmsg_instantly(recipient_number,msg)
    


# Configuration
smtp_server = "smtp.gmail.com"  # For Gmail. Use "smtp-mail.outlook.com" for Outlook.
port = 587  # For TLS
sender_email = os.environ.get('EMAIL_HOST_USER')  # Replace with your email
app_password = os.environ.get('EMAIL_HOST_PASSWORD')  # Replace with your app password



def send_mail(receiver_email,subject,body):
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        # Connect to the server
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()  # Secure the connection

        # Log in to your account
        server.login(sender_email, app_password)

        server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully!")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        server.quit()

def generate_verification_token():
    verification_token = secrets.token_urlsafe(64)
    return verification_token


def send_verifcation_link(receiver_email,verification_token):
    subject = 'verify your email please'
    verification_link = f"To verify your Email on EventEase Please press on the provided link https://127.0.0.1/verify-email?token={verification_token}"
    send_mail(receiver_email,subject,verification_link)