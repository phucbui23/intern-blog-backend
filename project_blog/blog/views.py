import json
from unicodedata import name

from django.core.paginator import Paginator
from django.forms import ValidationError
from rest_framework import filters
from rest_framework.decorators import api_view
from tag.models import BlogTag, Tag
from tag.serializers import TagSerializer
from user_account.models import User
from utils.api_decorator import json_response

from .models import Blog, BlogHistory, BlogLike
from .serializers import (BlogHistorySerializer, BlogLikeSerializer,
                          BlogSerializer)

@api_view(['POST'])
@json_response
def create_blog(request):
    data = request.data.copy()
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
    
    if tag is not None:
        for x in tag:
            # get tag by name in the list of tags
            tag_name = x.pop("name")
            _tag = Tag.get_tag_by_name(tag_name)
            
            # if tag not exist, create tag
            if _tag is None:
                _tag = Tag.objects.create(
                    author=user,
                    name=tag_name,
                    description="",
                )
                
            blogtag = BlogTag.get_blog_tag(new_blog, _tag)
            
            # create blogtag for every tag if not exist
            if blogtag is None:
                blogtag = BlogTag.objects.create(
                    blog=new_blog,
                    tag=_tag,
                )
    
    data = BlogSerializer(
        instance=new_blog, 
        many=False,
    ).data
    
    return data

@api_view(['GET'])
@json_response
def get_blogs(request):
    data = request.data.dict().copy()
    query_blogs_uid = data.pop('uid', None)
    query_blogs_title = data.pop('name', None)
    query_blogs_content = data.pop('content', None)

    if query_blogs_uid:
        return BlogSerializer( 
            Blog.objects.get(uid=query_blogs_uid),
            many=False
        ).data

    if query_blogs_title and query_blogs_content:
        query_blogs = Blog.objects.filter(
            name__icontains=query_blogs_title,
            content__icontains=query_blogs_content,
        )

    elif query_blogs_title:
        query_blogs = Blog.objects.filter(
            name__icontains=query_blogs_title,
        )

    elif query_blogs_content:
        query_blogs = Blog.objects.filter(
            content__icontains=query_blogs_content,
        )

    # paginator = Paginator(
    #     object_list=query_blogs, 
    #     per_page=3,
    # )

    # return BlogSerializer(
    #     instance={'data' : paginator}, 
    #     many=True,
    # ).data

    return BlogSerializer(
        query_blogs,
        many=True,
    ).data


@api_view(['GET'])
@json_response
def get_blog_detail(request):
    try:
        blog = Blog.objects.get(pk=request.GET.get('uid'))
    except Blog.DoesNotExist:
        raise ValidationError(
            message="Blog doesn't exist"
        )

    data = BlogSerializer(blog).data
    return data


@api_view(['POST'])
@json_response
def edit_blog(request):
    data = request.data.copy()
    
    try:
        blog = Blog.objects.get(
            pk=request.GET.get('uid'),
        )
    except Blog.DoesNotExist:
        raise ValidationError(
            message="Blog doesn't exist",
        )

    blog.name = data.pop('name', None)
    blog.content = data.pop('content', None)
    blog.is_published = data.pop('is_published', None)
    tag = data.pop('tag', None)
    
    if tag is not None:
        for x in tag:
            # get tag by name in the list of tags
            tag_name = x.pop("name")
            _tag = Tag.get_tag_by_name(tag_name)
            
            # if tag not exist, create tag
            if _tag is None:
                _tag = Tag.objects.create(
                    author=blog.author,
                    name=tag_name,
                    description="",
                )
                
            blogtag = BlogTag.get_blog_tag(blog, _tag)            
            # create blogtag for every tag if not exist
            if blogtag is None:
                blogtag = BlogTag.objects.create(
                    blog=blog,
                    tag=_tag,
                )
    
    blog.save()
    data = BlogSerializer(blog).data
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
