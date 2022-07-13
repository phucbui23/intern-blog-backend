from django.core.mail import EmailMessage
from django.forms import ValidationError
from django.template.loader import render_to_string
from email_logs.models import EmailLogs
from oauth.models import UserActivation, ResetPassword
from blog.models import Blog
from user_account.models import Follower
from .messages import INVALID_TYPE, SEND_FAIL
from .gen_token import gen_token
from .constant import DOMAIN
from .enums import Type

def send_email(user, type_email):
    token = gen_token()
    try:
        if (type_email == Type.ACTIVATE):
            subject = 'Activate Account'
            body = render_to_string(
                template_name='activate.html',
                context={
                    'user': user,
                    'domain': DOMAIN,
                    'token': token,
                }
            )
            to_user = [user.email]
            UserActivation.objects.create(
                author=user,
                token=token,
                active=True,
            )
        elif (type_email == Type.RESET_PASSWORD):   
            subject = 'Reset Password'
            body = render_to_string(
                template_name='reset.html',
                context={
                    'user': user,
                    'domain': DOMAIN,
                    'token': token,
                }
            )
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
        email.content_subtype = 'html'
        email.send()
    except: 
        raise ValueError(SEND_FAIL)
