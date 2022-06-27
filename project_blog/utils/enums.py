from enum import unique
from django.db import models


@unique
class Gender(models.TextChoices):
    MALE = 'MALE'
    FEMALE = 'FEMALE'
    OTHER = 'OTHER'

@unique
class Status(models.TextChoices):
    AVAILABLE='AVAILABLE'
    LOCKED = 'LOCKED'
    REMOVED = 'REMOVED'

@unique
class Type(models.TextChoices):
    ACTIVATE= 'ACTIVATE' 
    RESET_PASSWORD= 'RESET_PASSWORD' 
    FOLLOWER_POST= 'FOLLOWER_POST'

@unique
class Attachment_type(models.TextChoices):
    AVA = 'AVATAR'
    CVR = 'BLOG_COVER'
