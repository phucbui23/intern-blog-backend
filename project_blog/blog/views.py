from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models import Max
from django.forms import ValidationError
from rest_framework import filters
from rest_framework.decorators import api_view

from attachment.models import Attachment
from attachment.serializers import AttachmentSerializer
from tag.models import BlogTag, Tag
from tag.serializers import BlogTagSerializer, TagSerializer
from user_account.models import User
from user_account.serializers import UserSerializer
from utils.validate_token import validate_token
from utils.api_decorator import json_response, paginator
from utils.api_decorator import json_response
from utils.messages import (
    EMPTY_BLOG_STATUS, EMPTY_NAME_BLOG,
    TAG_NOT_EXIST, BLOG_NOT_EXIST,
    MAX_LENGTH_BLOG_NAME, MAX_LENGTH_BLOG_CONTENT,
    MAX_LENGTH_TAG_NAME,
)

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
    data = request.data.copy()
    validate_token(request.auth)
    user = request.user
    
    name = data.pop('name', None)
    content = data.pop('content', None)
    is_published = data.pop('is_published', None)
    
    if (name is None):
        raise ValidationError(EMPTY_NAME_BLOG)
    if (is_published is None):
        raise ValidationError(EMPTY_BLOG_STATUS)
    
    if (len(name) > 255):
        raise ValidationError(MAX_LENGTH_BLOG_NAME)
    if (len(content) > 255):
        raise ValidationError(MAX_LENGTH_BLOG_CONTENT)
    
    tags = data.pop('tag', None)
    attachments = data.pop('attachment', None)
    
    new_blog = Blog.objects.create(
        **data,
        name=name,
        content=content,
        author=user,
        is_published=is_published,
    )
    
    data = BlogSerializer(
        instance=new_blog, 
        many=False,
    ).data
    
    # create tag or add tag to blog if exist
    if tags is not None:
        for tag in tags:
            
            tag_name = tag.pop("name")
            if (len(tag_name) > 255):
                raise ValidationError(MAX_LENGTH_TAG_NAME)
        
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


@api_view(['POST'])
@json_response
@paginator
def get_blogs_by_tag(request):
    tag_name = request.POST.get('tag', None)
    
    if (len(tag_name) > 255):
        raise ValidationError(MAX_LENGTH_TAG_NAME)
    
    # check if tag exist
    try:
        tag = Tag.objects.get(
            name=tag_name,
        )
    except Tag.DoesNotExist:
        raise ValidationError(TAG_NOT_EXIST)
    
    blogs = Blog.objects.prefetch_related(
        'blogtag_fk_blog'
    ).filter(
        blogtag_fk_blog__tag=tag
    )
    
    blogs.order_by('-updated_at')
    
    return BlogSerializer(
        instance=blogs,
        many=True
    ).data


@api_view(['POST'])
@json_response
@paginator
def get_blogs(request):
    query_data = request.POST.get("keyword", '')

    if query_data is not '':
        query_blogs = Blog.objects.select_related(
            'author'
        ).filter(
            Q(author__username=query_data) |
            Q(uid__icontains=query_data) |
            Q(name__icontains=query_data) |
            Q(content__icontains=query_data)
        )

        query_blogs.order_by('-updated_at')

    else:
        query_blogs = Blog.objects.all().order_by('-created_at')

    # data = request.data.dict().copy()
    # query_blogs_uid = data.pop('uid', None)
    # query_blogs_title = data.pop('name', None)
    # query_blogs_content = data.pop('content', None)

    # if query_blogs_uid:
    #     return BlogSerializer( 
    #         Blog.objects.get(uid=query_blogs_uid),
    #         many=False
    #     ).data

    # if query_blogs_title and query_blogs_content:
    #     query_blogs = Blog.objects.filter(
    #         name__icontains=query_blogs_title,
    #         content__icontains=query_blogs_content,
    #     )

    # elif query_blogs_title:
    #     query_blogs = Blog.objects.filter(
    #         name__icontains=query_blogs_title,
    #     )

    # elif query_blogs_content:
    #     query_blogs = Blog.objects.filter(
    #         content__icontains=query_blogs_content,
    #     )

    # # paginator = Paginator(
    # #     object_list=query_blogs, 
    # #     per_page=3,
    # # )

    # # return BlogSerializer(
    # #     instance={'data' : paginator}, 
    # #     many=True,
    # # ).data

    return BlogSerializer(
        query_blogs,
        many=True,
    ).data


@api_view(['POST'])
@json_response
def get_blog_detail(request):
    bloguid = request.POST.get('uid', None)
    
    try:
        blog = Blog.objects.get(pk=bloguid)
    except Blog.DoesNotExist:
        raise ValidationError(BLOG_NOT_EXIST)
    
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
    
    # get number of likes of that blog
    num_like = BlogLike.objects.filter(
        blog=blog
    ).count()
    data['likes'] = num_like
    
    return data


@api_view(['POST'])
@json_response
def edit_blog(request):
    data = request.data.copy()
    validate_token(request.auth)
    user = request.user
    
    try:
        blog = Blog.objects.get(
            pk=request.GET.get('uid'),
        )
    except Blog.DoesNotExist:
        raise ValidationError(BLOG_NOT_EXIST)
        
    name = data.pop('name', blog.name)
    content = data.pop('content', blog.content)
    is_published = data.pop('is_published', blog.is_published)
    
    if (len(name) > 255):
        raise ValidationError(MAX_LENGTH_BLOG_NAME)
    if (len(content) > 255):
        raise ValidationError(MAX_LENGTH_BLOG_CONTENT)
    
    # change detail of blog
    blog.name = name
    blog.content = content
    blog.is_published = is_published
    blog.save()
        
    # create blog history when edit
    bloghistory = BlogHistory.objects.get(
        blog=blog,
        revision=1,
    )
    
    if BlogHistory.DoesNotExist:
        bloghistory = BlogHistory.objects.create(
            name=name,
            content=content,
            is_published=is_published,
            blog=blog,
            revision=1,
            author=user,
        )
    else:
        bloghistory = BlogHistory.objects.filter(
            blog=blog
        ).aggregate(Max('revision'))
        old_revision = bloghistory.revision
        
        # increase revision when edit
        blog_history = BlogHistory.objects.create(
            name=name,
            content=content,
            is_published=is_published,
            blog=blog,
            revision=old_revision+1,
            author=user,
        )
        
    # get list of tags in a blog before edit
    blog_tags = Tag.objects.prefetch_related(
        'blogtag_fk_tag'
    ).filter(
        blogtag_fk_tag__blog=blog
    )
    
    tags = data.pop('tag', None)
    
    for blog_tag in blog_tags:
        tag_existed = blog_tag.name
        tag_name = None
        
        for tag in tags:
            tag_name = tag.pop("name")
            
            if tag_name != tag_existed:
                continue
            
        if tag_name != tag_existed:
            blogtag_delete = BlogTag.objects.get(
                                blog=blog,
                                tag=tag_existed
                            ).delete()
    
    if tags is not None:
        for tag in tags:
            # get tag by name in the list of tags
            tag_name = tag.pop("name")
            tag_object = Tag.get_tag_by_name(tag_name)
                
            # if tag not exist, create tag
            if tag_object is None:
                tag_object = Tag.objects.create(
                    author=blog.author,
                    name=tag_name,
                    description="",
                )
                
            if tag_object not in blog_tags:
                new_blogtag = BlogTag.objects.create(
                    blog=blog,
                    tag=tag_object
                )
    
    return BlogSerializer(blog).data


@api_view(['POST'])
@json_response
def create_blog_like(request):
    validate_token(request.auth)
    user = request.user
    data = request.data.copy()
    bloguid = data.pop("blog", None)
    
    try:
        blog = Blog.objects.get(pk=bloguid)
    except Blog.DoesNotExist:
        raise ValidationError(BLOG_NOT_EXIST)
    
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
    validate_token(request.auth)
    user = request.user
    data = request.data.copy()
    bloguid = data.pop("blog", None)
    
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
    user = request.user
    validate_token(request.auth)
    data = request.GET.get('uid', None)
    
    blog = Blog.objects.get(
        author=user,
        pk=data
    ).delete()
    
    return None
