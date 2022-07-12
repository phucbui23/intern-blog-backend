from django.core.mail import EmailMessage
from django.forms import ValidationError
from email_logs.models import EmailLogs
from oauth.models import UserActivation, ResetPassword
from blog.models import Blog
from user_account.models import Follower
from utils.messages import INVALID_TYPE, SEND_FAIL
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
            to_user = [user.email]
            UserActivation.objects.create(
                author=user,
                token=token,
                active=True,
            )
        elif (type_email == Type.RESET_PASSWORD):   
            url = f'{DOMAIN}/reset?token={token}'
            subject = 'Reset Password'
            body = f'Hi {user.full_name} Please click this link to reset your password: {url}'
            to_user = [user.email]
            ResetPassword.objects.create(
                author=user,
                token=token,
                active=True,
            )
        
        elif (type_email == Type.FOLLOWER_POST):
            followers = list(Follower.objects.filter(author=user).values_list('follower__email', flat=True))
            blog = Blog.get_latest_blog(author=user)

            if (not followers):
                return None

            if (not blog):
                return None

            url = f'{DOMAIN}/detail?uid={blog.uid}'
            subject = f'Lastest Blog'
            body = f'{user.username} just post new blogs: {url}'
            to_user = followers

        else:
            raise ValidationError(INVALID_TYPE)

        followers = Follower.objects.filter(author=user)
        
        if (type_email == Type.FOLLOWER_POST):
            EmailLogs.send_follower_email(
                followers=followers, 
                subject=subject, 
                body=body
            )
            
        else:
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
            to=to_user,
        )
        email.send()
    except: 
        raise ValueError(SEND_FAIL)
