from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from django.core.validators import validate_email
from datetime import datetime, timedelta
from django.contrib.auth import password_validation
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from utils.api_decorator import json_response
from utils.send_email import send_email
from utils.enums import Type
from utils.validate_token import validate_token
from utils.messages import (
    EMPTY_PASSWORD_FIELDS,
    INVALID_TOKEN, NOT_ACTIVE, 
    EXPIRED_TOKEN, EMPTY_EMAIL_FIELDS, 
    ACCOUNT_ACTIVE, ACCOUNT_NOT_ACTIVE, WRONG_PASSWORD)
from user_account.models import User

from .models import UserActivation, UserDeviceToken, ResetPassword
from .serializers import UserDeviceTokenSerialier

# Create your views here.

@api_view(['PUT'])
@json_response
def activate(request):
    password = request.POST.get('password', None)

    if (not password):
        raise ValidationError(EMPTY_PASSWORD_FIELDS)

    password_validation.validate_password(password=password)
    try:
        token = UserActivation.objects.get(token=request.query_params['token'])
    except:
        raise ValidationError(INVALID_TOKEN)
    
    if (not token.active):
        raise Exception(NOT_ACTIVE)

    user = token.author
    UserActivation.objects.filter(author=user).update(active=False)
    expr = token.created_at + timedelta(minutes=5)   

    if (expr < datetime.now()):
        raise ValidationError(EXPIRED_TOKEN)

    token.active = True
    token.updated_at = datetime.now()
    token.save()

    user.set_password(password)
    user.active = True
    user.save()

    return True


@api_view(['POST'])
@json_response
def resend_email(request):
    email = request.POST.get('email', None)

    if (not email):
        raise ValidationError(EMPTY_EMAIL_FIELDS)
    
    validate_email(email)

    user = User.get_user(email=email)

    if (user.active):
        raise Exception(ACCOUNT_ACTIVE)
    
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
        raise ValidationError(EMPTY_EMAIL_FIELDS)
    
    if (not password):
        raise ValidationError(EMPTY_PASSWORD_FIELDS)

    validate_email(email)

    user = User.get_user(email=email) 

    if (not user.active):
        raise ValidationError(ACCOUNT_NOT_ACTIVE)

    if (not user.check_password(password)):
        raise ValidationError(WRONG_PASSWORD)    
    
    refresh = TokenObtainPairSerializer.get_token(user)
    UserDeviceToken.objects.filter(author=user).update(active=False)

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
        raise ValidationError(EMPTY_EMAIL_FIELDS)

    user = User.get_user(email=email)
    
    if (not user.active):
        raise ValidationError(ACCOUNT_NOT_ACTIVE)

    send_email(
        user=user, 
        type_email=Type.RESET_PASSWORD,
    )  
    
    return True


@api_view(['PUT'])
@json_response
def reset_password(request):
    password = request.POST.get('password', None)

    if (not password):
        raise ValidationError(EMPTY_PASSWORD_FIELDS)

    password_validation.validate_password(password=password)

    try:
        token = ResetPassword.objects.get(token=request.query_params['token'])
    except:
        raise ValidationError(INVALID_TOKEN)
    
    if (not token.active):
        raise Exception(NOT_ACTIVE)
    
    user = token.author

    ResetPassword.objects.filter(author=user).update(active=False)

    expr = token.created_at + timedelta(minutes=5)
    if ( expr < datetime.now()):
        raise ValidationError(EXPIRED_TOKEN)
    
    token.active=True,
    token.updated_at=datetime.now(),
    token.save()

    user.set_password(password)
    user.save()

    return True

@api_view(['PUT'])
@json_response
def log_out(request):
    token = validate_token(token=request.auth)
    token.active = False
    token.deactived_at = datetime.now()
    token.save()

    return True
