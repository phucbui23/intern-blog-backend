from django.core.mail import EmailMessage
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from email_logs.models import EmailLogs
from utils.enums import Type

def send_email(user, type_email):
    domain = '127.0.0.1:8000'
    subject = 'Activate Your Account'
    refresh = TokenObtainPairSerializer.get_token(user)
    if type_email == Type.ACTIVATE:
        url = f'http://{domain}/users/activate/{refresh.access_token}'
        body = 'Hi ' + user.full_name + 'Use link below to verify your email: ' + url
        
        EmailLogs.objects.create(
            author = user,
            type = type_email,
            subject = 'Activate User Account',
            content = 'Activate User Account',
        )

        email = EmailMessage(subject = subject, body= body, to=[user.email])
        email.send()
    
    elif type_email == Type.RESET_PASSWORD:   
        url = f'http://{domain}/users/reset/{refresh.access_token}'
        body = 'Hi ' + user.full_name + 'Please click this link to reset your password: ' + url
        
        EmailLogs.objects.create(
            author = user,
            type = type_email,
            subject = 'Reset Password',
            content = 'Reset Password',
        )

        email = EmailMessage(subject = subject, body= body, to=[user.email])
        email.send()