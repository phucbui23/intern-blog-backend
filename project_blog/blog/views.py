from django.forms import ValidationError
from rest_framework.decorators import api_view
from user_account.models import User
from utils.api_decorator import json_response

from .models import Blog, BlogHistory, BlogLike
from .serializers import (BlogHistorySerializer, BlogLikeSerializer,
                          BlogSerializer)


# Create your views here.
@api_view(['POST'])
@json_response
def create_blog(request):
    data = request.POST.dict().copy()
    username = data.pop('author', None)

    try:
        user = User.objects.get(
            username=username,
        )
    except User.DoesNotExist:
        raise ValidationError(
            message="doesn't exist"
        )
                                                                                 
    new_blog = Blog.objects.create(
        **data,
        author=user
    )

    data = BlogSerializer(
        instance=new_blog,
        many=False,
    ).data
    
    return data
