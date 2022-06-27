from enum import unique
from django.db import models


@unique
class Gender(models.TextChoices):
    MALE = 'MALE'
    FEMALE = 'FEMALE'
    OTHER = 'OTHER'

@unique
class Attachment_type(models.TextChoices):
    AVA = 'AVATAR'
    CVR = 'BLOG_COVER'
