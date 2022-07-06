from datetime import datetime
from django.contrib.auth import password_validation
from django.core.validators import validate_email
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError,NotFound

from utils.api_decorator import json_response
from utils.send_email import send_email
from utils.enums import Type

from .models import User
from .serializers import UserSerializer



@api_view(['POST'])
@json_response
def sign_up(request):
    email = request.POST.get('email', None)
    fullname = request.POST.get('full_name', None)
    nickname = request.POST.get('nick_name', fullname)

    if (not email):
        raise ValidationError('Users must have email address')
    if (not fullname):
        raise ValidationError('Users must have full name')

    validate_email(email)

    try:
        is_has_user = User.get_user(email=email).exists()
    except NotFound:
        is_has_user = False

    if (is_has_user):
        raise ValidationError('Email is existed')

    username = email.split('@')[0]
    user = User.objects.create( 
        email=email, 
        username=username,
        full_name=fullname,
        nick_name=nickname,
        active=False,
        is_superuser=False,
        is_admin=False,
    )
    
    send_email(
        user=user, 
        type_email=Type.ACTIVATE,
    )

    return UserSerializer(
        instance=user,
        many=False
    ).data


@api_view(['PUT'])
@json_response
def edit_profile(request):
    user = request.user
    user.phone_number = request.POST.get('phone_number', user.phone_number)
    user.full_name = request.POST.get('full_name', user.full_name)
    user.nick_name = request.POST.get('nick_name', user.nick_name)
    user.quote = request.POST.get('quote', user.quote)
    user.gender = request.POST.get('gender', user.gender)
    user.updated_at = datetime.now()
    user.save()

    return UserSerializer(
        instance= user,
        many = False
    ).data


@api_view(['PUT'])
@json_response
def change_password(request):
    user = request.user
    current_password = request.POST.get('current_password', None)
    new_password = request.POST.get('new_password', None)
    validate_password = request.POST.get('validate_password', None)

    password_validation.validate_password(new_password)

    if not current_password or not new_password or not validate_password:
        raise ValidationError('Please fill all fields!!!')
 
    if not user.check_password(current_password):
        raise ValidationError('Wrong password')
    
    if new_password != validate_password:
        raise ValidationError('Validate password must be same as new password')
    
    user.set_password(new_password)
    user.save()

    return UserSerializer(
        instance= user,
        many = False
    ).data
    