from django.core.mail import EmailMessage
from django.forms import ValidationError
from email_logs.models import EmailLogs
from oauth.models import UserActivation, ResetPassword
from .gen_token import gen_token
from .constant import DOMAIN
from .enums import Type

def send_email(user, type_email):
    token = gen_token()
    try:
        if (type_email == Type.ACTIVATE):
            url = f'{DOMAIN}/activateaccount?token={token}'
            subject = 'Activate Account'
            body = f'Hi {user.full_name} Use link below to verify your email: {url}'
            
            UserActivation.objects.create(
                author=user,
                token=token,
                active=True,
            )
        elif (type_email == Type.RESET_PASSWORD):   
            url = f'{DOMAIN}/reset?token={token}'
            subject = 'Reset Password'
            body = f'Hi {user.full_name} Please click this link to reset your password: {url}'

            ResetPassword.objects.create(
                author=user,
                token=token,
                active=True,
            )
        
        else:
            raise ValidationError('Type is not valid')
        

        EmailLogs.objects.create(
            author=user,
            type=type_email,
            is_success=True,
            subject=subject,
            content=body,
        )

        email = EmailMessage(
            subject=subject, 
            body=body, 
            to=[user.email],
        )
        email.send()
    except: 
        raise ValueError('Send Email Failed')
