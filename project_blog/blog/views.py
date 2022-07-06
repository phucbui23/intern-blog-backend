import re
from unicodedata import name

from django.core.paginator import Paginator
from django.forms import ValidationError
from rest_framework import filters
from rest_framework.decorators import api_view

from tag.models import BlogTag, Tag
from tag.serializers import TagSerializer, BlogTagSerializer
from user_account.models import User
from utils.api_decorator import json_response

from .models import Blog, BlogHistory, BlogLike
from .serializers import (
    BlogHistorySerializer, 
    BlogLikeSerializer,
    BlogSerializer
)

@api_view(['POST'])
@json_response
def create_blog(request):
    user = request.user
    data = request.data.copy()
    tags = data.pop('tag', None)
    
    new_blog = Blog.objects.create(
        **data,
        author=user,
    )
    
    # if tags is not None:
    for tag in tags:
            # get tag by name in the list of tags
            tag_name = tag.pop("name")
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
    
    return BlogSerializer(
        instance=new_blog, 
        many=False,
    ).data


@api_view(['GET'])
@json_response
def get_blogs_by_tag(request):
    data = request.GET.dict().copy()
    tagname = data.pop('tag', None)
    
    # check if blog exist
    try:
        tag = Tag.objects.get(
            name=tagname,
        )
    except Tag.DoesNotExist:
        raise ValidationError(
            message="Tag doesn't exist"
        )
    
    blogs = BlogTag.objects.filter(
        tag=tag,
    )
    
    return BlogTagSerializer(
        instance=blogs,
        many=True,
    ).data


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
    bloguid = request.GET.get('uid')
    try:
        blog = Blog.objects.get(pk=bloguid)
    except Blog.DoesNotExist:
        raise ValidationError(
            message="Blog doesn't exist"
        )
        
    # join tables to get tag
    tags = Tag.objects.prefetch_related(
        'blogtag_fk_tag'
    ).filter(
        blogtag_fk_tag__blog=blog
    )
    
    data = BlogSerializer(blog).data
    data['tags'] = TagSerializer(
        instance=tags,
        many=True
    ).data
    
    return data

@api_view(['POST'])
@json_response
def edit_blog(request):
    user = request.user
    
    data = request.data.copy()
    
    try:
        blog = Blog.objects.get(
            pk=request.GET.get('uid'),
        )
    except Blog.DoesNotExist:
        raise ValidationError(
            message="Blog doesn't exist",
        )

    blog.name = data.pop('name', blog.name)
    blog.content = data.pop('content', blog.content)
    blog.is_published = data.pop('is_published', blog.is_published)
    blog.save()
    
    tags = data.pop('tag', None)
    removed_tags = data.pop('-tag', None)
    
    if tags is not None:
        for tag in tags:
            # get tag by name in the list of tags
            tag_name = tag.pop("name")
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
                
    if removed_tags is not None:
        for tag in removed_tags:
            tag_name = tag.pop("name")
            _tag = Tag.get_tag_by_name(tag_name)
                
            blogtag = BlogTag.get_blog_tag(blog, _tag).delete()

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
