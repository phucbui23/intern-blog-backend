from django.db import models
from user_account.models import User

# Create your models here.
class UserDeviceToken(models.Model):
    author = models.ForeignKey(
        to=User, 
        on_delete=models.CASCADE,
        to_field='id',
        related_name='user_device_token_fk_author',
        db_column='author_id',
        db_constraint=False, # accessing a related object that doesn’t exist will raise DoesNotExist 
        null=False,
        blank=False
    )

    token = models.CharField(
        max_length=255, 
    )

    device_id = models.CharField(
        max_length=255, 
        null=True,
        blank=True,
    )

    device_token = models.CharField(
        max_length=255, 
        null=True,
        blank=True,
    )

    device_model = models.CharField(
        max_length=255, 
        null=True,
        blank=True
    )

    user_agent = models.TextField(
        null=True,
        blank=True,
    )

    active = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    deactivated_at = models.DateTimeField(
        null=True,
        blank=True,
        auto_now=True,
    )

    class Meta:
        unique_together = (
            ('author', 'token',),
        )
    
    @staticmethod
    def get_user_device(user):
        try:
            data = UserDeviceToken.objects.filter(author=user)
        except:
            raise
        return data

    def __str__(self) -> str:
        return self.author.email

class UserActivation(models.Model):
    author = models.ForeignKey(
        to= User, 
        on_delete=models.CASCADE,
        to_field='id',
        related_name='user_activation_fk_author',
        db_column='author_id',
        db_constraint=False,
        null= False,
        blank=False,
    )

    active = models.BooleanField(
        default=False,
    )

    token = models.CharField(
        max_length=255, 
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        null=True,
        blank=True,
    )

    class Meta:
        unique_together= (
            ('author', 'token',),
        )

    def __str__(self) -> str:
        return self.author.email

class ResetPassword(models.Model):
    author = models.ForeignKey(
        to= User, 
        on_delete=models.CASCADE,
        to_field='id',
        related_name='reset_password_fk_author',
        db_column='author_id',
        db_constraint=False,
        null=False,
        blank=False,
    )

    active = models.BooleanField(
        default=False,
    )

    token = models.CharField(
        max_length=255, 
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        null=True,
        blank=True,
    )

    class Meta:
        unique_together= (
            ('author', 'token',),
        )

    def __str__(self) -> str:
        return self.author.email
