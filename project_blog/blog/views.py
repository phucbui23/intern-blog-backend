import re
from unicodedata import name

from django.core.paginator import Paginator
from django.forms import ValidationError
from rest_framework import filters
from rest_framework.decorators import api_view

from attachment.models import Attachment
from attachment.serializers import AttachmentSerializer
from tag.models import BlogTag, Tag
from tag.serializers import TagSerializer
from user_account.models import User
from user_account.serializers import UserSerializer
from utils.messages import TAG_NOT_EXIST, BLOG_NOT_EXIST
from utils.api_decorator import json_response

from .models import (
    Blog, 
    BlogAttachment, 
    BlogHistory, 
    BlogLike
)
from .serializers import (
    BlogHistorySerializer, 
    BlogLikeSerializer,
    BlogSerializer
)

@api_view(['POST'])
@json_response
def create_blog(request):
    # user = request.user
    data = request.data.copy()
    
    _user = data.pop('author', None)
    user = User.objects.get(username=_user)
    
    tags = data.pop('tag', None)
    attachments = data.pop('attachment', None)
    
    new_blog = Blog.objects.create(
        **data,
        author=user,
    )
    
    # create tag or add tag to blog if exist
    if tags is not None:
        for tag in tags:
            # get tag by name in the list of tags
            tag_name = tag.pop("name")
            _tag = Tag.get_tag_by_name(tag_name)
            
            # if tag not exist, create tag
            if _tag is None:
                _tag = Tag.objects.create(
                    author=user,
                    name=tag_name,
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
    
    # add attachment to the blog
    if attachments is not None:
        for attachment in attachments:
            attachment_uid = attachment.pop("uid")
            
            new_attachment = Attachment.get_attachment(
                attachment_uid
            )
            
            blog_attachment = BlogAttachment.objects.create(
                blog=new_blog,
                attachment=new_attachment,
            )
    
    return data


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
            message=TAG_NOT_EXIST
        )
    
    blogs = Blog.objects.prefetch_related(
        'blogtag_fk_blog'
    ).filter(
        blogtag_fk_blog__tag=tag
    )
    
    data = BlogSerializer(
        instance=blogs,
        many=True
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
    bloguid = request.GET.get('uid')
    
    try:
        blog = Blog.objects.get(pk=bloguid)
    except Blog.DoesNotExist:
        raise ValidationError(
            message=BLOG_NOT_EXIST
        )
        
    num_like = BlogLike.objects.filter(
        blog=blog
    ).count()
    
    data = BlogSerializer(blog).data
        
    # join tables to get tag
    tags = Tag.objects.prefetch_related(
        'blogtag_fk_tag'
    ).filter(
        blogtag_fk_tag__blog=blog
    )
    
    data['tags'] = TagSerializer(
        instance=tags,
        many=True
    ).data
    
    # get attachments in a blog
    attachments = Attachment.objects.prefetch_related(
        'blogattachment_fk_attachment'
    ).filter(
        blogattachment_fk_attachment__blog=blog
    )
    
    data['attachments'] = AttachmentSerializer(
        instance=attachments,
        many=True
    ).data
    
    # get author detail
    author = User.objects.get(
        id = blog.author.id
    )
    
    data['author'] = UserSerializer(
        instance=author,
        many=False
    ).data
    
    data['likes'] = num_like
    
    return data


@api_view(['POST'])
@json_response
def edit_blog(request):
    data = request.data.copy()
    
    # user = request.user
    _user = data.pop('author', None)
    user = User.objects.get(username=_user)
    
    try:
        blog = Blog.objects.get(
            pk=request.GET.get('uid'),
        )
    except Blog.DoesNotExist:
        raise ValidationError(
            message=BLOG_NOT_EXIST,
        )
        
    try:
        check = (blog.author==user)
    except check is False:
        raise ValidationError(
            message="This user is not author"
        )
        
    name = data.pop('name', blog.name)
    content = data.pop('content', blog.content)
    is_published = data.pop('is_published', blog.is_published)
        
    # create blog history when edit
    # bloghistory = BlogHistory.objects.get(
    #     blog=blog,
    #     revision=1,
    # )
    # if BlogHistory.DoesNotExist:
    #     bloghistory = BlogHistory.objects.create(
    #         name=name,
    #         content=content,
    #         is_published=is_published,
    #         blog=blog,
    #         revision=1,
    #         author=user,
    #     )
    # else:
    #     old_revision = bloghistory.revision
    #     # increase revision when edit
    #     blog_history = BlogHistory.objects.create(
    #         name=name,
    #         content=content,
    #         is_published=is_published,
    #         blog=blog,
    #         revision=old_revision+1,
    #         author=user,
    #     )
        
    # get list of tags in a blog before edit
    blog_tags = Tag.objects.prefetch_related(
        'blogtag_fk_tag'
    ).filter(
        blogtag_fk_tag__blog=blog
    )

    # change detail of blog
    blog.name = data.pop('name', blog.name)
    blog.content = data.pop('content', blog.content)
    blog.is_published = data.pop('is_published', blog.is_published)
    blog.save()
    
    tags = data.pop('tag', None)
    print(blog_tags[0].name)
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
    
    return BlogSerializer(blog).data


@api_view(['POST'])
@json_response
def create_blog_like(request):
    # user = request.user
    data = request.data.copy()
    bloguid = data.pop("blog", None)
    
    userid = data.pop("author", None)
    user = User.objects.get(id=userid)
    
    try:
        blog = Blog.objects.get(pk=bloguid)
    except Blog.DoesNotExist:
        raise ValidationError(
            message=BLOG_NOT_EXIST
        )
    
    bloglike = BlogLike.objects.create(
        **data,
        author=user,
        blog=blog,
    )
    
    data = BlogLikeSerializer(bloglike).data
    
    data['blog'] = BlogSerializer(
        instance=blog,
        many=False
    ).data
    
    # get author detail    
    data['author'] = UserSerializer(
        instance=user,
        many=False
    ).data
    
    return data


@api_view(['DELETE'])
@json_response
def blog_unlike(request):
    # user = request.user
    data = request.data.copy()
    bloguid = data.pop("blog", None)
    
    userid = data.pop("author", None)
    user = User.objects.get(id=userid)
    
    try:
        blog = Blog.objects.get(pk=bloguid)
    except Blog.DoesNotExist:
        raise ValidationError(
            message=BLOG_NOT_EXIST
        )
    
    bloglike = BlogLike.objects.get(
        author=user,
        blog=blog,
    ).delete()
    
    return None


@api_view(['DELETE'])
@json_response
def delete_blog(request):
    # user = request.user
    data = request.GET.get('uid', None)
    
    
    
    blog = Blog.objects.get(
        pk=data
    ).delete()
    
    return None
