from django.forms import ValidationError
from rest_framework.decorators import api_view

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from user_account.models import User, Follower
from user_account.serializers import UserSerializer, FollowerSerializer
from utils.api_decorator import json_response
from django.contrib.sites.shortcuts import get_current_site

from utils.send_email import send_email
from oauth.models import UserActivation
from oauth.models import UserDeviceToken
from email_logs.models import EmailLogs
from oauth.serializers import UserDeviceTokenSerialier
from oauth.serializers import UserActivationSerialier

import jwt
SECRET_KEY = 'django-insecure-cvkqf4x_zg5--)q6^o5z8nfwm!+$0v31co+dbr%vmm2oq_#a7x'

# Create your views here.


@api_view(['POST'])
@json_response
def sign_up(request):
    username = request.POST.get('username', None)
    email = request.POST.get('email', None)
    password = request.POST.get('password', None)
    
    if not email:
        raise ValueError('Users must have email address')
    
    if not password:
        raise ValueError('Users must have password')

    user = User.objects.create( 
        username = username, 
        email = email,
    )
    user.set_password(password)

    current_site = get_current_site(request)
    subject = 'Activate Your Account'
    refresh = TokenObtainPairSerializer.get_token(user)

    domain = current_site.domain

    url = f'http://{domain}/users/activate/{refresh.access_token}'
    email_body = 'Hi ' + user.username + 'Use link below to verify your email: ' + url
    
    
    data = {'email_body': email_body, 'email_subject':subject, 'to_email': user.email}
    
    send_email(data)  

    EmailLogs.objects.create(
        author = user,
        subject = 'Activate User Account',
        content = 'Activate User Account',
    )
    
    return UserSerializer(
            instance=user,
            many=False
        ).data


@api_view(['GET'])
@json_response
def activate(request, token):
    
    payload = jwt.decode(
        jwt=token, 
        key=SECRET_KEY, 
        algorithms=['HS256'],
        )
    user_id = payload['user_id']
    user = User.objects.get(pk = user_id)
    
    user.active = True
    user.save()

    logs = EmailLogs.objects.filter(author__pk = user_id)[0]
    logs.is_success = True
    logs.save()         

    activate_user = UserActivation.objects.create(
        author = user,
        active = True,
        token = token
    )
    return UserActivationSerialier(
            instance=activate_user,
            many=False
        ).data

@api_view(['POST'])
@json_response
def log_in(request):
    username = request.POST.get('username', None)
    email = request.POST.get('email', None)
    password = request.POST.get('password', None)

    if (not email):
        raise ValueError('Users must have email address')
    
    if (not password):
        raise ValueError('Users must have password')

    user = User.objects.get(email=email)
    
    if (not user.active):
        raise ValidationError(
            message= 'Please validate your account'
        )

    refresh = TokenObtainPairSerializer.get_token(user)

    device_token = UserDeviceToken.objects.create(
        author=user,
        token=refresh.access_token,
        active=True
    )

    return UserDeviceTokenSerialier(
            instance=device_token,
            many=False
        ).data

