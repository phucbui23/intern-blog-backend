from django.forms import ValidationError
from rest_framework.decorators import api_view

from utils.api_decorator import json_response
from user_account.models import User
from blog.models import Blog

from .models import Tag, BlogTag
from .serializers import TagSerializer


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


@api_view(['GET'])
@json_response
def get_tag_in_blog(request):
    data = request.GET.dict().copy()
    bloguid = data.pop('blog', None)
    blogtags = BlogTag.get_tags_in_blog(bloguid)
    
    # check if blog exist
    try:
        blog = Blog.objects.get(
            uid=bloguid,
        )
    except Blog.DoesNotExist:
        raise ValidationError(
            message="Blog doesn't exist"
        )
    
    data = [] # use list for tags of blog
    for blogtag in blogtags:
        tag = Tag.get_tag_by_name(blogtag.tag)
        tagdata = TagSerializer(tag).data
        data.append(tagdata)
        
    return data
