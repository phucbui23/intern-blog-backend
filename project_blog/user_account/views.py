from datetime import datetime

from blog.models import Blog, BlogLike
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound, ValidationError
from utils.api_decorator import json_response, paginator
from utils.enums import Type
from utils.messages import (ACCOUNT_ACTIVE, ACCOUNT_NOT_ACTIVE, NOT_FOUND_BLOG,
                            NOT_FOUND_USER, NOT_SAME_PASSWORD, WRONG_PASSWORD)
from utils.send_email import send_email
from utils.validate_input import (validate_email, validate_fullname,
                                  validate_nickname, validate_password,
                                  validate_phone_number)

from .models import Follower, User
from .serializers import FollowerSerializer, UserSerializer


@api_view()
@json_response
def get_user_info(request):
    author_email = request.GET.get('author_email', None)
    user = request.user
    if (author_email):
        author = User.get_user(email=author_email)

        data = UserSerializer(
            instance=author,
            many=False,
        ).data

        if (isinstance(user, User)):
            is_followed = Follower.objects.filter(
                author=author,
                follower=user,
                active=True,    
            ).exists()
            data['is_followed'] = is_followed

    else:
        blog =  Blog.objects.filter(author=user, is_published=True)
        blog_num = blog.count()
        like_num = 0
        for each_blog in blog:
            like_num += BlogLike.objects.filter(blog=each_blog).count()
            
        follow_num = Follower.objects.filter(author=user, active=True).count()

        data = UserSerializer(
            instance=user,
            many=False,
        ).data

        data['blog_numbers'] = blog_num
        data['like_numbers'] = like_num
        data['follow_numbers'] = follow_num

    return data


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
        exist_user = User.get_user(email=email)
        if (exist_user.active):
            raise ValidationError(ACCOUNT_ACTIVE)
        else:
            raise ValidationError(ACCOUNT_NOT_ACTIVE)
    except NotFound:

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
    try:
        author_email = request.POST.get('email')
        author = User.get_user(email=author_email)
    except User.DoesNotExist:
        raise NotFound(NOT_FOUND_USER)
    
    try:
        data = Follower.objects.get(
            author=author,
            follower=request.user,
            follow_by=None,
        )

        data.active = not data.active
        data.save()

    except Follower.DoesNotExist:
        data = Follower.objects.create(
            author=author,
            follower=request.user,
            follow_by=None,
            active=True,
        )

    return FollowerSerializer(
        instance=data,
        many=False,
    ).data

@api_view(['GET'])
@json_response
@paginator
def get_user_following(request):

    user=request.user

    # users that author follows
    following = Follower.objects.filter(
        follower=user,
        active=True,
        follow_by=None,
    )

    try:
        for follow in following:
            follower = follow.author
            total_blog = Blog.get_total_blog_by_user(follower)
            most_liked_blog = BlogLike.get_most_liked_blog(follower)

            setattr(follow, 'total_blog', total_blog)
            setattr(follow, 'most_liked_blog', most_liked_blog)

    except Exception as e:
        print(e)

    data = FollowerSerializer(
        instance=following,
        many=True,
    ).data

    return data
