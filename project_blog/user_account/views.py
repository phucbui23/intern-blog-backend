from email import message
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from utils.api_decorator import json_response
from user_account.models import User, Follower
from user_account.serializers import UserSerializer, FollowerSerializer
# Create your views here.


@api_view(['POST'])
@json_response
def create_user(request):
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)

    user = User.objects.create_user(
        username=username,
        password=password,
    )

    data = {
        "data": UserSerializer(
            instance=user,
            many=False
        ).data,
        "error_code": 0,
        "message": "success",
    }

    return data
    return Response(data=data, status=status.HTTP_201_CREATED)

    # serializer = UserSerialier(data=request.POST)
    # if serializer.is_valid():
    #     user = serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_follower(request):
    # if request.method == 'GET':
    #     followers = Follower.objects.all()
    #     serializer = FollowerSerializer(followers, many=True)
    #     return Response(serializer.data)
    # elif request.method == 'POST':
    serializer = FollowerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
