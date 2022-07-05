from django.forms import ValidationError
from rest_framework.decorators import api_view

from user_account.models import User
from blog.models import Blog
from .models import Tag, BlogTag
from .serializers import BlogTagSerializer, TagSerializer
from blog.serializers import BlogSerializer
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
    data = request.GET.dict().copy()
    name = data.pop('name', None)
    model = Tag.get_tag_by_name(name)
    
    data = TagSerializer(model).data
    return data


@api_view(['GET'])
@json_response
def get_tag_by_blog(request):
    data = request.GET.dict().copy()
    blog = data.pop('blog', None)
    tags = BlogTag.get_all_tag_by_blog(blog)
    
    # use list for tags of blog
    data = []
    for x in tags:
        tag = Tag.get_tag_by_name(x.tag)
        data.append(TagSerializer(tag).data)
        
    return data


@api_view(['POST'])
@json_response
def edit_tag(request):
    data = request.data.copy()
    try:
        tag = Tag.objects.get(name=request.GET.get('tag'))
    except Tag.DoesNotExist:
        raise ValidationError(
            message="Tag doesn't exist",
        )
        
    tag.name = data.pop('name', None)
    tag.description = data.pop('description', None)
    tag.save()
    
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