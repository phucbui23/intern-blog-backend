from django.forms import ValidationError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from user_account.models import User
from blog.models import Blog
from .models import Tag
from .serializers import TagSerializer
from utils.api_decorator import json_response


@api_view(['POST'])
@json_response
def create_tag(request):    
    data = request.POST.dict().copy()
    username = data.pop('author', None)
    
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


@api_view(['GET', 'PUT', 'DELETE'])
@json_response
def get_tag(request):
    tag = Tag.objects.get(pk=request.GET.get('id'))
    data = TagSerializer(tag).data
    return data