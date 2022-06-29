from pickle import PUT
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from user_account.models import User, Follower
from user_account.serializers import UserSerialier, FollowerSerializer
from utils.api_decorator import json_response
# Create your views here.


@api_view(['POST'])
@json_response
def create_user(request):
    user = User.objects.create(
        **request.POST.dict()
    )

    user.save()
    return UserSerialier(
            instance=user,
            many=False
        ).data

@api_view()
@json_response
def get_list_user(request):
    users = User.objects.all()
    return UserSerialier(
        instance=users,
        many = True).data


@api_view([PUT])
@json_response

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
