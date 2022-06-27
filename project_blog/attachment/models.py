import uuid

from django.db import models

# Create your models here.


class Attachment(models.Model):
    TYPE_CHOICES = [
        ('AVA', 'AVATAR'),
        ('CVR', 'BLOG_COVER'),
    ]
    uid = models.CharField(
        default=uuid.uuid4(),
        primary_key=True,
        editable=False, unique=True, max_length=36)
    # user = models.ForeignKey('User', on_delete=models.CASCADE)
    type = models.CharField(max_length=32, choices=TYPE_CHOICES)
    file_name = models.CharField(max_length=225)
    display_name = models.CharField(max_length=225)
    file_path = models.TextField()
    deleted_at = models.DateTimeField(null=True)
    delete = models.BooleanField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(null=True)
