from random import randint
from django.conf import settings
from twilio.rest import Client
# import pywhatkit

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