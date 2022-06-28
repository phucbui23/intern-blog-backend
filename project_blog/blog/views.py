# from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
# from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from .models import Blog, BlogHistory, BlogLike
from .serializers import (BlogHistorySerializer, BlogLikeSerializer,
                          BlogSerializer)


# Create your views here.
@api_view(['POST'])
def create_blog(request):
    data = request.data
    serializer = BlogSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

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
