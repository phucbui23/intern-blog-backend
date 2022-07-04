from django.forms import ValidationError
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from utils.api_decorator import json_response

from .models import Blog, BlogHistory, BlogLike
from .serializers import (BlogHistorySerializer, BlogLikeSerializer, BlogSerializer)
from user_account.models import User
from tag.views import create_tag, create_blogtag, get_tag


@api_view(['POST'])
@json_response
def create_blog(request):
    data = request.data.dict().copy()
    username = data.pop('author', None)
    tag = data.pop('tag', None)
    
    # check if user exists or not
    try:
        user = User.objects.get(
            username=username,
        )
    except User.DoesNotExist:
        raise ValidationError(
            message="User doesn't exist",
        )
        
    new_blog = Blog.objects.create(
        **data,
        author=user,
    )
    
    if tag != None:
        for x in tag:
            ...
            # create_tag()
            # create_blogtag()
    
    data = BlogSerializer(
        instance=new_blog, 
        many=False,
    ).data
    
    return data


@api_view(['GET'])
@json_response
def get_blog(request):
    try:
        blog = Blog.objects.get(pk=request.GET.get('uid'))
    except Blog.DoesNotExist:
        raise ValidationError(
            code=500,
            message="Blog doesn't exist"
        )

    data = BlogSerializer(blog).data
    return data


@api_view(['PUT'])
@json_response
def edit_blog(request):
    data = request.data.dict().copy()
    
    try:
        blog = Blog.objects.get(
            pk=request.GET.get('uid'),
        )
    except Blog.DoesNotExist:
        raise ValidationError(
            message="Blog doesn't exist",
        )

    new_blog = Blog.objects.update(
        **data,
    )
    
    data = BlogSerializer(
        data=new_blog, 
        many=False,
    ).data
    
    return data

# @api_view(['POST'])
# def create_blog_history(request):
#     data = JSONParser().parse(request)
#     serializer = BlogHistorySerializer(data=data)
#     if serializer.is_valid():
#         serializer.save()
#         return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
#     return JsonResponse(serializer.data, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# def create_blog_like(request):
#     data = JSONParser().parse(request)
#     serializer = BlogLikeSerializer(data=data)
#     if serializer.is_valid():
#         serializer.save()
#         return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
#     return JsonResponse(serializer.data, status=status.HTTP_400_BAD_REQUEST)
