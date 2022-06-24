from django.db import models
from blog.project_blog.user_account.models import User
from blog.project_blog.blog.models import Blog

class Tag(models.Model):
    name = models.TextField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(null=True)
    
class BlogTag(models.Mode):
    id = models.IntegerField()
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(null=True)
    
    class Meta:
        unique_together = ('blog', 'tag',)