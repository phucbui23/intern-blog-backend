from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from user_account.models import User, Follower
from user_account.serializer import UserSerialier, FollowerSerializer
# Create your views here.


@api_view(['GET','POST'])
def create_user(request):
    # if request.method == 'GET':
    #     users = User.objects.all()
    #     serializer = UserSerialier(users, many=True)
    #     return Response(serializer.data)
    # elif request.method == 'POST':
        serializer = UserSerialier(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def create_follower(request):
    # if request.method == 'GET':
    #     followers = Follower.objects.all()
    #     serializer = FollowerSerializer(followers, many=True)
    #     return Response(serializer.data)
    # elif request.method == 'POST':
        serializer = FollowerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
        