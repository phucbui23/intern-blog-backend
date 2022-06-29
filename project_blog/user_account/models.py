from django.db import models
from utils.enums import Gender
from utils.enums import Status
#from blog.models import Blog
#from attachment.models import Attachment
# Create your models here.

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not username:
            raise ValueError('Users must have an email address')
        user = self.model(
            username=username,
        )
        user.set_password(password)
        user.is_superuser = False
        user.is_admin = False
        user.active = False
        user.save(using=self._db)
        return user
    def create_staffuser(self, username, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            password=password,
            username=username,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
    def create_superuser(self, username, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            password=password,
            username=username,
        )
        user.is_superuser = True
        user.is_admin = True
        user.active = True
        user.save(using=self._db)
        return user
class User(AbstractBaseUser):
    objects = UserManager()
    REQUIRED_FIELD = ('username',)
    USERNAME_FIELD = 'username'
    username = models.CharField(max_length=255, unique=True)
    email = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    phone_number = models.CharField(
        max_length=16,
        null=True,
        blank=True,
    )
    full_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    nick_name = models.CharField(
        max_length=255,
        null=True,
    )
    quote = models.TextField(
        null=True,
        blank=True,
    )
    gender = models.CharField(
        max_length=12,
        null=True,
        blank=True,
        choices=Gender.choices,
        default=Gender.OTHER,
    )
    avatar = models.ForeignKey(
        to='attachment.Attachment',
        on_delete=models.CASCADE,
        to_field='uid',
        related_name='user_fk_avatar',
        db_column='avatar_uid',
        db_constraint=False,
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.AVAILABLE,
    )
    active = models.BooleanField()
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        null=True,
        blank=True,
    )
    is_superuser = models.BooleanField()
    is_admin = models.BooleanField()

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, perm, obj=None):
        return True


class Follower(models.Model):
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        to_field='id',
        related_name='follower_fk_author',
        db_column='author_id',
        db_constraint=False,
        null=False,
        blank=False,
    )
    follower = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        to_field='id',
        related_name='follower_fk_follower',
        db_column='follower_id',
        db_constraint=False,
        null=False,
        blank=False,
    )
    follow_by = models.ForeignKey(
        to='blog.Blog',
        on_delete=models.CASCADE,
        to_field='uid',
        related_name='follower_fk_follower_by',
        db_column='follower_by_uid',
        db_constraint=False,
        null=True,
        blank=True,
    )
    active = models.BooleanField()
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        null=True,
        blank=True,
    )
