from django.db import models


# Create your models here.


class User(models.Model):
    GENDER_TYPES = (('Female', 'Female'), ('Male', 'Male'), ('Other', 'Other'))
    STATUS_TYPES = (('AVAILABLE', 'AVAILABLE'),
                    ('LOCKED', 'LOCKED'), ('REMOVED', 'REMOVED'))
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=16, null=True)
    full_name = models.CharField(max_length=255, null=True)
    nick_name = models.CharField(max_length=255, null=True)
    quote = models.TextField(null=True)
    gender = models.CharField(max_length=12, null=True, choices=GENDER_TYPES)
    # avatar = models.ForeignKey('Attachment', null=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=16)
    active = models.BooleanField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(null=True)
    is_superuser = models.BooleanField()
    is_admin = models.BooleanField()


class Follower(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower_fk_author',
    )
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower_fk_follower',
    )
    # follow_by = models.ForeignKey('Blog', null=True, on_delete=models.CASCADE)
    active = models.BooleanField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(null=True)



