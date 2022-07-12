from django.core.paginator import Paginator
from django.db.models import Q, Prefetch
from django.db.models import Max
from django.forms import ValidationError
from rest_framework import filters
from rest_framework.decorators import api_view

from attachment.models import Attachment
from attachment.serializers import AttachmentSerializer
from tag.models import BlogTag, Tag
from tag.serializers import TagSerializer
from user_account.models import User
from user_account.serializers import UserSerializer
from utils.api_decorator import json_response, paginator
from utils.messages import *

from .models import (
    Blog, 
    BlogAttachment, 
    BlogHistory, 
    BlogLike
)
from .serializers import (
    BlogLikeSerializer,
    BlogSerializer
)


@api_view(['POST'])
@json_response
@paginator
def get_matrix_blogs(request):
    search = request.POST.get("search", None)
    uid = request.POST.get("uid", None)

    blog_records = Blog.objects.all()

    if search is not None:
        blog_records = blog_records.select_related(
            'author'
        ).filter(
            Q(author__username=search) |
            Q(uid__icontains=search) |
            Q(name__icontains=search) |
            Q(content__icontains=search)
        )

    if not (uid is None):
        blog_records = blog_records.filter(
            uid=uid
        )

    blog_records = blog_records.prefetch_related(
        Prefetch(
            'blogtag_fk_blog',
            to_attr='tags'
        ),
        Prefetch(
            'blogattachment_fk_blog',
            to_attr='attachment'
        )
    )


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

    # # return BlogSerializer(
    # #     instance={'data' : paginator}, 
    # #     many=True,
    # # ).data

    return BlogSerializer(
        blog_records,
        many=True,
    ).data


@api_view(['POST'])
@json_response
def create_blog(request):
    user = request.user
    data = request.data.copy()
    
    name = data.pop('name', None)
    content = data.pop('content', None)
    is_published = data.pop('is_published', None)
    
    if (name is None):
        raise ValidationError(EMPTY_NAME_BLOG)
    if (is_published is None):
        raise ValidationError(EMPTY_BLOG_STATUS)
    
    if (len(name) > 255):
        raise ValidationError(MAX_LENGTH_BLOG_NAME)
    if content and (len(content) > 255):
        raise ValidationError(MAX_LENGTH_BLOG_CONTENT)
    
    tags_name = data.pop('tags', [])
    attachments_uid = data.pop('attachments', [])
    
    new_blog = Blog.objects.create(
        **data,
        name=name,
        content=content if (content) else None,
        author=user,
        is_published=is_published,
    )
    
    # xu ly tags
    if (len(tags_name) > 0):
        new_blog_tags = []
        
        for tag_name in tags_name:
            new_tag, created = Tag.objects.get_or_create(name=tag_name)
                
            new_blog_tags.append(
                BlogTag(
                    blog=new_blog,
                    tag=new_tag,
                )
            )
                
        BlogTag.objects.bulk_create(
            objs=new_blog_tags,
            ignore_conflicts=True
        )
        
    # xu ly attachments
    if (len(attachments_uid) > 0):
        new_blog_attachments = []
        
        for attachment_uid in attachments_uid:
            new_attachment = Attachment.objects.get(uid=attachment_uid)
                
            new_blog_attachments.append(
                BlogAttachment(
                    blog=new_blog,
                    tag=new_attachment,
                )
            )
                
        BlogAttachment.objects.bulk_create(
            objs=new_blog_attachments,
            ignore_conflicts=True
        )
    
    return BlogSerializer(
        instance=new_blog, 
        many=False,
    ).data


@api_view(['POST'])
@json_response
@paginator
def get_blogs_by_tag(request):
    tag_name = request.POST.get('tag', '')
    
    if (tag_name != ''):
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
        
    else:
        blogs = Blog.objects.all().order_by('-created_at')
    
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
    
    data = BlogSerializer(
            query_blogs,
            many=True,
        ).data
    
    for query_blog in query_blogs:
        blog_attachments = BlogAttachment.objects.filter(
            blog=query_blog,
        )
        
        blog_attachments_uid = blog_attachments.values_list(
            'attachment__uid',
            flat=True,
        )
        
        author = User.objects.get(
            id=query_blog.author.id
        )
        
        # print(UserSerializer(author).data)
    
    return data


@api_view(['POST'])
@json_response
def get_blog_detail(request):
    bloguid = request.POST.get('uid', None)
    
    try:
        blog = Blog.objects.get(pk=bloguid)
    except Blog.DoesNotExist:
        raise ValidationError(BLOG_NOT_EXIST)
    
    data = BlogSerializer(blog).data
    
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
        id=blog.author.id
    )
    
    data['author'] = UserSerializer(
        instance=author,
        many=False
    ).data
    
    return data


@api_view(['POST'])
@json_response
def edit_blog(request):
    user = request.user
    data = request.data.copy()
    
    uid = request.query_params.get('uid', None)
    if (uid is None):
        raise ValidationError(
            message=UID_REQUIRED
        )
    
    blog = Blog.get_by_uid(uid=uid)
    
    blog.name = data.pop('name', blog.name)
    blog.content = data.pop('content', blog.content)
    blog.is_published = data.pop('is_published', blog.is_published)
     
    blog.is_valid()
    
    # Xu ly tags
    tags_name = data.pop('tags', [])
    
    current_blog_tags = BlogTag.objects.filter(
        tag__name__in=tags_name,
        blog=blog,
    )
        
    current_blog_tags_name = current_blog_tags.values_list(
        'tag__name',
        flat=True,
    )

    remove_blog_tags = BlogTag.objects.filter(
        blog=blog
    ).exclude(
        tag__name__in=tags_name
    )
        
    new_blog_tags = []
        
    for tag_name in tags_name:
        if not (tag_name in current_blog_tags_name):
            new_tag, created = Tag.objects.get_or_create(name=tag_name)
                
            new_blog_tags.append(
                BlogTag(
                    blog=blog,
                    tag=new_tag,
                )
            )
                
    BlogTag.objects.bulk_create(
        objs=new_blog_tags,
        ignore_conflicts=True
    )
        
    remove_blog_tags.delete()
    
    # Xu ly attachments
    attachments_uid = data.pop('attachments', [])
    
    current_blog_attachments = BlogAttachment.objects.filter(
        attachment__uid__in=attachments_uid,
        blog=blog,
    )
        
    current_blog_attachments_uid = current_blog_attachments.values_list(
        'attachment__uid',
        flat=True,
    )

    remove_blog_attachments = BlogAttachment.objects.filter(
        blog=blog
    ).exclude(
        attachment__uid__in=attachments_uid
    )
        
    new_blog_attachments = []
        
    for attachment_uid in attachments_uid:
        if not (attachment_uid in current_blog_attachments_uid):
            new_attachment = Attachment.objects.get(uid=attachment_uid)
            
            new_blog_attachments.append(
                BlogAttachment(
                    blog=blog,
                    attachment=new_attachment,
                )
            )
                
    BlogAttachment.objects.bulk_create(
        objs=new_blog_attachments,
        ignore_conflicts=True
    )
        
    remove_blog_attachments.delete()

    blog.save()
    
    return BlogSerializer(blog).data


@api_view(['POST'])
@json_response
def create_blog_like(request):
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
    data = request.GET.get('uid', None)
    
    blog = Blog.objects.get(
        author=user,
        pk=data
    ).delete()
    
    return None


@api_view()
@json_response
@paginator
def get_user_blog(request):
    user = request.user

    blogs = Blog.objects.filter(
        author=user,
        is_published=True,
    )

    return BlogSerializer(
        instance=blogs,
        many=True
    ).data


@api_view()
@json_response
@paginator
def get_follower_blog(request):
    ...



@api_view()
@json_response
@paginator
def get_new_blog(request):
    ...
