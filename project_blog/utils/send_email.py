from django.core.mail import EmailMessage
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from email_logs.models import EmailLogs

def send_email(user):
    
    domain = '127.0.0.1:8000'
    subject = 'Activate Your Account'
    refresh = TokenObtainPairSerializer.get_token(user)
    
    url = f'http://{domain}/users/activate/{refresh.access_token}'
    body = 'Hi ' + user.full_name + 'Use link below to verify your email: ' + url
    
    EmailLogs.objects.create(
        author = user,
        subject = 'Activate User Account',
        content = 'Activate User Account',
    )

    email = EmailMessage(subject = subject, body= body, to=[user.email])
    email.send()