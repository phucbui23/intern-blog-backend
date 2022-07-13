from attachment.models import Attachment
from attachment.serializers import AttachmentSerializer

from django.db import models
from django.db.models import Prefetch, Q
from django.forms import ValidationError
from rest_framework.decorators import api_view

from notification.models import Notification
from user_account.models import Follower
from tag.models import BlogTag, Tag
from user_account.models import User
from user_account.serializers import UserSerializer
from utils.api_decorator import json_response, paginator
from utils.enums import Notification_type, Type
from utils.messages import *
from utils.send_email import send_email

from .models import Blog, BlogAttachment, BlogHistory, BlogLike
from .serializers import BlogLikeSerializer, BlogSerializer


@api_view(['POST'])
@json_response
@paginator
def get_matrix_blogs(request):
    search = request.POST.get("search", None) # search by keyword

    uid = request.POST.get("uid", None)
    tag = request.POST.get("tag", None)
    
    following = request.POST.get("following", None) # get blogs of user following
    author_email = request.POST.get("author_email", None) # get blogs of a user

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

    if uid is not None:
        blog_records = blog_records.filter(
            uid=uid,
        )
        
        return BlogSerializer(
            instance=blog_records,
            many=False,
        ).data

    elif tag is not None:
        blog_records = Blog.objects.prefetch_related(
            'blogtag_fk_blog'
        ).filter(
            blogtag_fk_blog__tag__name__icontains=tag
        ).order_by('-updated_at')

    elif following is not None:
        user = request.user

        user_following = Follower.objects.filter(
            follower=user,
            active=True,
            follow_by=None,
        )

        temp_blog_records = Blog.objects.none()

        for follow in user_following:
            temp_blog_records |= blog_records.filter(
                author=follow.author,
            )

        blog_records = temp_blog_records.order_by('-created_at')

    elif search is not None:
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
        
    elif author_email is not None:
        user = request.user

        # author_email = request.POST.get('author_email', None)
        author = User.get_user(email=author_email)

        author_blogs = Blog.objects.filter(
                author=author
            ).prefetch_related(
                'bloglike_fk_blog'
            ).annotate(
                like=models.Count('bloglike_fk_blog')
            ).order_by(
                '-like'
            )

        blog_records = BlogSerializer(
            instance=author_blogs,
            many=True,
        ).data

        # check if user likes and follows blogs of the author
        if isinstance(user, User):
            for each_blog in blog_records:
                is_follow = Follower.objects.filter(
                    author=author,
                    follower=user,
                    follow_by=each_blog['uid'],
                    active=True,    
                ).exists()
                each_blog['is_follow'] = is_follow

                is_liked = BlogLike.objects.filter(
                    author=user,
                    blog=each_blog['uid'],
                ).exists()
                each_blog['is_liked'] = is_liked
            
        else:
            for each_blog in blog_records:
                each_blog['is_follow'] = False
                each_blog['is_liked'] = False

        return blog_records

    return BlogSerializer(
        instance=blog_records,
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
    attachment_file_path = data.pop('attachments', [])
    
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
    if (len(attachment_file_path) > 0):        
        new_attachment = Attachment.objects.get(
            file_path__in=attachment_file_path
        )
                
        BlogAttachment.objects.create(
            blog=new_blog,
            attachment=new_attachment,
        )
    
    followers = Follower.objects.filter(
        author=user
    )
    send_email(
        user=user, 
        type_email=Type.FOLLOWER_POST
    )
    
    for follower in followers:
        follower_user = follower.follower
        
        new_noti = Notification.objects.create(
            type=Notification_type.FOLLOWER_NEW_POST,
            author=follower_user,
            blog=new_blog,
            is_success=True,
            subject='Có bài viết mới',
            content=user.full_name+' vừa thêm bài viết mới',
        )
    
    return BlogSerializer(
        instance=new_blog, 
        many=False,
    ).data


@api_view(['POST'])
@json_response
@paginator
def get_blogs_by_tag(request):
    user = request.user
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
        
        blogs.order_by('-updated_at')
        
    else:
        blogs = Blog.objects.all().order_by('-created_at')
    
    blog_records = BlogSerializer(
        instance=blogs,
        many=True,
    ).data
    
    if isinstance(user, User):
        for each_blog in blog_records:
            author_email = each_blog['author']['email']
            author = User.get_user(email=author_email)
            
            is_follow = Follower.objects.filter(
                author=author,
                follower=user,
                follow_by=each_blog['uid'],
                active=True,    
            ).exists()
            each_blog['is_follow'] = is_follow

            is_liked = BlogLike.objects.filter(
                author=user,
                blog=each_blog['uid'],
            ).exists()
            each_blog['is_liked'] = is_liked
            
    else:
        for each_blog in blog_records:
            each_blog['is_follow'] = False
            each_blog['is_liked'] = False
    
    return blog_records

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
    
    user = request.user

    if isinstance(user, User):
        is_followed = Follower.objects.filter(
            author=author,
            follower=user,
            follow_by=blog,
            active=True,
        ).exists()
        data['is_followed'] = is_followed

        is_liked = BlogLike.objects.filter(
            author=user,
            blog=blog,
        ).exists()
        data['is_liked'] = is_liked
        
    else:
        data['is_followed'] = False
        data['is_liked'] = False

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
        attachment__file_path__in=attachments_uid,
        blog=blog,
    )
        
    current_blog_attachments_file_path = current_blog_attachments.values_list(
        'attachment__file_path',
        flat=True,
    )

    remove_blog_attachments = BlogAttachment.objects.filter(
        blog=blog
    ).exclude(
        attachment__file_path__in=attachments_uid
    )
        
    new_blog_attachments = []
        
    for attachment_file_path in attachments_uid:
        if not (attachment_file_path in current_blog_attachments_file_path):
            new_attachment = Attachment.objects.get(file_path=attachment_file_path)
            
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
    
    new_noti = Notification.objects.create(
        type=Notification_type.BLOG_LIKED,
        author=user,
        blog=blog,
        is_success=True,
        subject='Bài viết của bạn được yêu thích',
        content='Bài viết "'+blog.name
            +'" của bạn đã được yêu thích bởi '+user.full_name,
    )
    
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
    )

    return BlogSerializer(
        instance=blogs,
        many=True
    ).data


@api_view()
@json_response
@paginator
def get_new_blog(request):
    blogs = Blog.objects.all().order_by('-created_at')

    return BlogSerializer(
        instance=blogs,
        many=True,
    ).data
    

@api_view(['GET'])
@json_response
def get_blog_likes(request):
    blog_uid = request.query_params.get('blog_uid', None)
    
    try:
        blog = Blog.objects.get(uid=blog_uid)
    except Blog.DoesNotExist:
        raise ValidationError(
            message=BLOG_NOT_EXIST
        )
        
    blog_likes = BlogLike.objects.filter(
        blog=blog
    )
        
    return BlogLikeSerializer(
        instance=blog_likes,
        many=True
    ).data
