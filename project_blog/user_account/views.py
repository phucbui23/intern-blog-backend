from django.forms import ValidationError
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from rest_framework.decorators import api_view

from user_account.models import User, Follower
from user_account.serializers import UserSerialier, FollowerSerializer
from utils.api_decorator import json_response
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect

from utils.send_email import send_email
from utils.token import token_generator
from oauth.models import UserActivation
from oauth.models import UserDeviceToken
from email_logs.models import EmailLogs
from oauth.serializers import UserDeviceTokenSerialier

# Create your views here.


@api_view(['POST'])
@json_response
def create_user(request):
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
    token = token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    domain = current_site.domain

    url = f'http://{domain}/users/activate/{uid}/{token}'
    email_body = 'Hi ' + user.username + 'Use link below to verify your email: ' + url
    
    
    data = {'email_body': email_body, 'email_subject':subject, 'to_email': user.email}
    
    send_email(data)  

    EmailLogs.objects.create(
        author = user,
        subject = 'Activate User Account',
        content = 'Activate User Account',
    )

    return UserSerialier(
            instance=user,
            many=False
        ).data


@api_view(['GET'])
def activate(request, uid, token):
    uid = force_str(urlsafe_base64_decode(uid))
    user = User.objects.get(pk=uid)

    if token_generator.check_token(user,token):
        user.active = True
        user.save()

        logs = EmailLogs.objects.filter(author__pk = uid)[0]
        logs.is_success = True
        logs.save()         

        UserActivation.objects.create(
            author = user,
            active = True,
            token = token
        )
    return redirect('/users/login')

@api_view(['POST'])
@json_response
def login(request):
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

    token = token_generator.make_token(user=user)
    device_token = UserDeviceToken.objects.create(
        author=user,
        token=token,
        active=True
    )

    return UserDeviceTokenSerialier(
            instance=device_token,
            many=False
        ).data


@api_view()
def log_out(request):
    ...

@api_view(['POST'])
def create_follower(request): ...
    # if request.method == 'GET':
    #     followers = Follower.objects.all()
    #     serializer = FollowerSerializer(followers, many=True)
    #     return Response(serializer.data)
    # elif request.method == 'POST':
    # serializer = FollowerSerializer(data=request.data)
    # if serializer.is_valid():
    #     serializer.save()
    #     return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    # return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
