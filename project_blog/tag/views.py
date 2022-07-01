from django.db import IntegrityError
from django.forms import ValidationError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from user_account.models import User
from blog.models import Blog
from .models import Tag, BlogTag
from .serializers import BlogTagSerializer, TagSerializer
from utils.api_decorator import json_response


@api_view(['POST'])
@json_response
def create_tag(request):    
    data = request.POST.dict().copy()
    username = data.pop('author', None)
    
    # check if user exists
    try:
        user = User.objects.get(
            username=username,
        )
    except User.DoesNotExist:
        raise ValidationError(
            message="Doesn't exist"
        )
        
    new_tag = Tag.objects.create(
        **data,
        author=user,
    )
    
    data = TagSerializer(
        instance=new_tag, 
        many=False,
    ).data
    
    return data



@api_view(['GET'])
@json_response
def get_tag(request):
    try:
        # get tag by id
        tag = Tag.objects.get(pk=request.GET.get('id'))
        
        # get tag by name
        # tag = Tag.objects.get(name=request.GET.get('name'))
    except Tag.DoesNotExist:
        raise ValidationError(
            code=500,
            message="Tag doesn't exist"
        )

    data = TagSerializer(tag).data
    return data


@api_view(['POST'])
@json_response
def create_blogtag(request):    
    data = request.POST.dict().copy()
    bloguid = data.pop('blog', None)
    tagid = data.pop('tag', None)
    
    # check if blog exists
    try:
        blog = Blog.objects.get(
            uid=bloguid,
        )
    except Blog.DoesNotExist:
        raise ValidationError(
            code=500,
            message="Blog doesn't exist"
        )
        
    # check if tag exists
    try:
        tag = Tag.objects.get(
            id=tagid,
        )
    except Tag.DoesNotExist:
        raise ValidationError(
            code=500,
            message="Tag doesn't exist"
        )
        
    blogtag = BlogTag.objects.create(
        **data,
        blog=blog,
        tag=tag,
    )
        
    data = BlogTagSerializer(
        instance=blogtag, 
        many=False,
    ).data
            
    return data