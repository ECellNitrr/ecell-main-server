from decouple import config
from random import randint
import requests
import http.client
from django.core.mail import send_mail
from django.conf import settings

def send_otp(contact, **kwargs):
    otp = str(randint(1000, 9999))
    if 'otp' in kwargs:
        otp = kwargs['otp']
    message = "Your OTP for E-Cell NIT Raipur portal is {}.".format(otp)
    
    if settings.MOCK_SMS_EMAIL:
        print('\n===================== Mock SMS =====================\n')
        print(f'Contact: {contact}')
        print(f'Message: {message}')
        print('\n====================================================\n')
    else:
        conn = http.client.HTTPSConnection("api.msg91.com")
        contact = str(contact)
        authkey = config('authkey')
        url = "https://api.msg91.com/api/sendhttp.php?mobiles={}&authkey={}&route=4&sender=SUMMIT&message={}&country=91".format(contact,authkey,message)
        conn.request("GET",url)
        res = conn.getresponse()
        data = res.read()
    
    return otp


def send_email_otp(recipient_list, **kwargs):
    otp = str(randint(1000, 9999))
    if 'otp' in kwargs:
        otp = kwargs['otp']
    
    email_from = settings.EMAIL_HOST_USER
    message = "Your OTP for E-Cell NIT Raipur portal is {}.".format(otp)
    subject = 'E-Cell NITRR'

    if settings.MOCK_SMS_EMAIL:
        print('\n===================== Mock email service =====================\n')
        print(f'Recipients: {recipient_list}')
        print(f'Subject: {subject}')
        print(f'Body: {message}')
        print('\n==============================================================\n')
    else:
        send_mail( subject, message, email_from, recipient_list )
    return otp

