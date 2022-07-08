from datetime import datetime
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError,NotFound

from utils.api_decorator import json_response
from utils.send_email import send_email
from utils.enums import Type
from utils.validate_token import validate_token
from utils.validate_input import (
    validate_email, validate_password,
    validate_fullname, validate_nickname, validate_phone_number)
from utils.messages import (
    EXIST_USER, WRONG_PASSWORD, 
    NOT_SAME_PASSWORD, NOT_FOUND_BLOG, NOT_FOUND_USER
    )
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

    validate_email(email=email)
    validate_fullname(full_name=fullname)
    validate_nickname(nick_name=nickname)

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
    
    validate_phone_number(phone_number=phone_number)
    validate_fullname(full_name=full_name)
    validate_nickname(nick_name=nick_name)
    
    
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
    new_password_again = request.POST.get('new_password_again', None)

    validate_password(current_password)
    validate_password(new_password)

    if not user.check_password(current_password):
        raise ValidationError(WRONG_PASSWORD)
    
    if new_password != new_password_again:
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