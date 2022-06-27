from django.db import models


class Blog(models.Model):
    uid = models.UUIDField(
        primary_key=True, editable=False, max_length=36, unique=True)
    name = models.TextField(max_length=255)
    # author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(null=True)
    is_published = models.BooleanField()
    published_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(null=True)


class BlogHistory(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    revision = models.IntegerField()
    # author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField(max_length=255)
    content = models.TextField(null=True)
    is_published = models.BooleanField()
    published_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(null=True)

    class Meta:
        unique_together = (
            ('blog', 'revision',),
        )


class BlogLike(models.Model):
    # author = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    comment = models.TextField(null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(null=True)

    # class Meta:
    #     unique_together = ('author', 'blog',)
