from django.forms import ValidationError
from rest_framework.decorators import api_view

from utils.api_decorator import json_response
from user_account.models import User
from blog.models import Blog

from .models import Tag, BlogTag
from .serializers import BlogTagSerializer, TagSerializer


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
            message="User doesn't exist"
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
