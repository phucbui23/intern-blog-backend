from rest_framework.decorators import api_view

from django.contrib.auth import password_validation
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from user_account.models import User
from utils.api_decorator import json_response

from utils.send_email import send_email
from .models import UserActivation, UserDeviceToken, ResetPassword
from email_logs.models import EmailLogs
from .serializers import UserDeviceTokenSerialier, ResetPasswordSerialier

from utils.enums import Type
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.exceptions import ValidationError

from django.core.validators import validate_email
from datetime import datetime, timedelta

# Create your views here.

@api_view(['PUT'])
@json_response
def activate(request, token):
    password = request.POST.get('password', None)

    if (not password):
        raise ValueError('Password must not be empty')

    password_validation.validate_password(password=password)

    try:
        token = UserActivation.objects.get(token=token)
    except:
        raise Exception('Token is invalid')
    
    if (not token.active):
        raise Exception('Not active')

    user = token.author
    UserActivation.objects.filter(author=user).update(active=False)
    expr = token.created_at + timedelta(minutes=5)   ##check
    if expr < datetime.now():
        raise Exception('Token is expired')

    UserActivation.objects.update(
        author=user,
        token=token,
        active=True,
        updated_at=datetime.now(),
    )

    user.active = True
    user.save()

    return True


@api_view(['POST'])
@json_response
def resend_email(request):
    email = request.POST.get('email', None)
    user = User.objects.get(email=email)

    if (not email):
        raise ValidationError('Users must have email address')
    
    validate_email(email)

    send_email(
        user=user, 
        type_email=Type.ACTIVATE,
    )

    return True

@api_view(['POST'])
@json_response
def log_in(request):
    email = request.POST.get('email', None)
    password = request.POST.get('password', None)

    if (not email):
        raise ValidationError('Users must have email address')
    
    if (not password):
        raise ValidationError('Users must have password')

    validate_email(email)

    user = User.get_user(email=email) 

    if (not user.active):
        raise ValidationError(
            'Please validate your account'
        )

    if (user.check_password(password)):
        raise Exception(
            'Wrong Password'
        )    
    
    refresh = TokenObtainPairSerializer.get_token(user)

    device_token = UserDeviceToken.objects.create(
        author=user,
        token=refresh.access_token,
        active=True,
    )
    
    
    return UserDeviceTokenSerialier(
        instance=device_token,
        many=False
    ).data


@api_view(['POST'])
@json_response
def forgot_password(request):
    email = request.POST.get('email', None)

    if (not email):
        raise ValidationError('Users must have email address')

    user = User.get_user(email=email)
    
    if (not user.active):
        raise ValidationError(
             'Please check your email and validate your account'
        )

    send_email(
        user=user, 
        type_email=Type.RESET_PASSWORD,
    )  
    
    return True


@api_view(['PUT'])
@json_response
def reset_password(request, token):
    password = request.POST.get('password', None)

    if (not password):
        raise ValueError('Password must not be empty')

    password_validation.validate_password(password=password)

    try:
        token = ResetPassword.objects.get(token=token)
    except:
        raise Exception('Token is invalid')
    
    if (not token.active):
        raise Exception('Not active')
    
    user = token.author

    ResetPassword.objects.filter(author=user).update(active=False)

    if (token.created_at < datetime.now()):
        raise Exception('Token is expired')
    
    ResetPassword.objects.create(
        author=user,
        token=token,
        active=True,
        created_at=datetime.now(),
    )

    user.set_password(password)
    user.save()

    return True