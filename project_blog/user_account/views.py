from datetime import datetime
from django.contrib.auth import password_validation
from django.core.validators import validate_email
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError,NotFound

from utils.api_decorator import json_response
from utils.send_email import send_email
from utils.enums import Type
from utils.validate_token import validate_token
from utils.messages import (
    MAX_LENGTH_PHONE_NUMBER, MAX_LENGTH_EMAIL, MAX_LENGTH_FULLNAME, MAX_LENGTH_NICK_NAME,
    MAX_LENGTH_PASSWORD, EXIST_USER, EMPTY_FIELDS,
    EMPTY_EMAIL_FIELDS, EMPTY_FULLNAME_FIELDS, 
    WRONG_PASSWORD, NOT_SAME_PASSWORD, NOT_FOUND_BLOG, NOT_FOUND_USER)
from blog.models import Blog

from .models import User, Follower
from .serializers import FollowerSerializer, UserSerializer



@api_view()
@json_response
def get_user_info(request):
    validate_token(token=request.auth)
    user = User.objects.get(email=request.user.email)
    
    return UserSerializer(
        instance=user,
        many=False,
    ).data


@api_view(['POST'])
@json_response
def sign_up(request):
    email = request.POST.get('email', None)
    fullname = request.POST.get('full_name', None)
    nickname = request.POST.get('nick_name', fullname)

    if (not email):
        raise ValidationError(EMPTY_EMAIL_FIELDS)
    if (not fullname):
        raise ValidationError(EMPTY_FULLNAME_FIELDS)

    if (len(email) > 255):
        raise ValidationError(MAX_LENGTH_EMAIL)
    
    if (len(fullname) > 255):
        raise ValidationError(MAX_LENGTH_FULLNAME)
    
    if (len(nickname) > 255):
        raise ValidationError(MAX_LENGTH_NICK_NAME)

    validate_email(email)

    try:
        User.get_user(email=email)
        is_has_user = True
    except NotFound:
        is_has_user = False

    if (is_has_user):
        raise ValidationError(EXIST_USER)

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
        many=False,
    ).data


@api_view(['PUT'])
@json_response
def edit_profile(request):
    validate_token(request.auth)
    
    user = request.user

    phone_number = request.POST.get('phone_number', user.phone_number)
    full_name = request.POST.get('full_name', user.full_name)
    nick_name = request.POST.get('nick_name', user.nick_name)
    
    if (phone_number and len(phone_number) > 16):
        raise ValidationError(MAX_LENGTH_PHONE_NUMBER)
    
    if (full_name and len(full_name) > 255):
        raise ValidationError(MAX_LENGTH_FULLNAME)
    
    if (nick_name and len(nick_name) > 255):
        raise ValidationError(MAX_LENGTH_NICK_NAME)
    
    
    user.phone_number = phone_number
    user.full_name = full_name
    user.nick_name = nick_name
    user.quote = request.POST.get('quote', user.quote)
    user.gender = request.POST.get('gender', user.gender)
    user.updated_at = datetime.now()
    user.save()

    return UserSerializer(
        instance=user,
        many=False
    ).data


@api_view(['PUT'])
@json_response
def change_password(request):
    validate_token(request.auth)

    user = request.user
    current_password = request.POST.get('current_password', None)
    new_password = request.POST.get('new_password', None)
    validate_password = request.POST.get('validate_password', None)

    password_validation.validate_password(new_password)

    if not current_password or not new_password or not validate_password:
        raise ValidationError(EMPTY_FIELDS)
    
    if not user.check_password(current_password):
        raise ValidationError(WRONG_PASSWORD)
    
    if (len(new_password) > 255):
        raise ValidationError(MAX_LENGTH_PASSWORD)

    if new_password != validate_password:
        raise ValidationError(NOT_SAME_PASSWORD)
    
    user.set_password(new_password)
    user.save()

    return UserSerializer(
        instance=user,
        many=False
    ).data
    


@api_view(['PUT'])
@json_response
def follow_by_blog(request):
    validate_token(request.auth)

    try:
        uid_blog = request.POST.get('blog_uid')
        blog = Blog.objects.get(uid=uid_blog)
    except Blog.DoesNotExist:
        raise NotFound(NOT_FOUND_BLOG)
    
    blog_author = blog.author

    try:
        data = Follower.objects.get(
            author=blog_author,
            follower=request.user,
            follow_by=blog,
        )

        data.active = not data.active
        data.save()

    except Follower.DoesNotExist:
        data = Follower.objects.create(
            author=blog_author,
            follower=request.user,
            follow_by=blog,
            active=True,
        )

    return FollowerSerializer(
        instance=data,
        many=False,
    ).data

@api_view(['PUT'])
@json_response
def follow_user(request):
    validate_token(request.auth)

    try:
        author_email = request.POST.get('email')
        author = User.get_user(email=author_email)
    except User.DoesNotExist:
        raise NotFound(NOT_FOUND_USER)
    
    try:
        data = Follower.objects.get(
            author=author,
            follower=request.user,
        )

        data.active = not data.active
        data.save()

    except Follower.DoesNotExist:
        data = Follower.objects.create(
            author=author,
            follower=request.user,
            active=True,
        )

    return FollowerSerializer(
        instance=data,
        many=False,
    ).data