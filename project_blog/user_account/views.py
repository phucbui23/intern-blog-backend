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
from utils.enums import Type
import jwt
from project_blog.settings import SECRET_KEY



@api_view(['POST'])
@json_response
def sign_up(request):
    email = request.POST.get('email', None)
    fullname = request.POST.get('full_name', None)
    nickname = request.POST.get('nick_name', None)
    
    if (not email):
        raise ValueError('Users must have email address')
    is_has_user = User.objects.filter(email=email)
    if (is_has_user):
        raise ValueError('Email is existed')

    user = User( 
        email=email, 
    )
    user.full_name = fullname
    user.nick_name = nickname
    user.save()

    send_email(user=user)

    return UserSerializer(
            instance=user,
            many=False
        ).data


@api_view(['POST'])
@json_response
def activate(request, token):
    password = request.POST.get('password', None)

    if (not password):
        raise ValueError('Password must not be empty')
    
    payload = jwt.decode(
        jwt=token, 
        key=SECRET_KEY, 
        algorithms=['HS256'],
        )

    
    user_id = payload['user_id']
    user = User.objects.get(pk = user_id)
    user.set_password(password)
    user.active = True
    user.save()

    logs = EmailLogs.objects.filter(author__pk=user_id)[0]
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
    email = request.POST.get('email', None)
    password = request.POST.get('password', None)

    if (not email):
        raise ValueError('Users must have email address')
    
    if (not password):
        raise ValueError('Users must have password')

    user = User.objects.get(email=email)
    
    if (not user.active):
        send_email(user=user)
        raise ValidationError(
            message= 'Please check your email and validate your account'
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


@api_view(['PUT'])
@json_response
def edit_profile(request):
    print(request.auth)
    user = request.user
    user.phone_number = request.POST.get('phone_number', None)
    user.full_name = request.POST.get('full_name', None)
    user.nick_name = request.POST.get('nick_name', None)
    user.quote = request.POST.get('quote', None)
    user.gender = request.POST.get('gender', None)
    #user.avatar = request.POST.get('avatar', None)
    user.save()

    return UserSerializer(
        instance= user,
        many = False
    ).data

@api_view(['PUT'])
@json_response
def change_password(request):
    user = request.user
    password = request.POST.get('password', None)
    new_password = request.POST.get('new_password', None)
    validate_password = request.POST.get('validate_password', None)

    if not password or not new_password or not validate_password:
        raise ValueError('Please fill all fields!!!')

    if password != user.password:
        raise ValueError('Wrong password')
    
    if new_password != validate_password:
        raise ValueError('Validate password must be same as new password')
    
    user.set_password(new_password)
    user.save()

    return UserSerializer(
        instance= user,
        many = False
    ).data
    


@api_view(['PUT'])
@json_response
def reset_password(request):
    user = request.user
    current_site = get_current_site(request)
    subject = 'Activate Your Account'
    refresh = TokenObtainPairSerializer.get_token(user)

    domain = current_site.domain

    url = f'http://{domain}/users/reset/{refresh.access_token}'
    email_body = 'Please click link below to reset your password: ' + url
    
    
    data = {'email_body': email_body, 'email_subject':subject, 'to_email': user.email}
    
    send_email(data)  

    EmailLogs.objects.create(
        author = user,
        type = Type.RESET_PASSWORD,
        subject = 'Reset Password',
        content = 'Reset Password',
    )
    
    return UserSerializer(
            instance=user,
            many=False
        ).data






