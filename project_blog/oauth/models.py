from django.db import models
from user_account.models import User

# Create your models here.
class UserDeviceToken(models.Model):
    # author = models.ForeignKey('User', unique=True, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    device_id = models.CharField(max_length=255, null=True)
    device_token = models.CharField(max_length=255, null=True)
    device_model = models.CharField(max_length=255, null=True)
    user_agent = models.TextField(null=True)
    active = models.BooleanField()
    created_at = models.DateTimeField()
    deactivated_at = models.DateTimeField(null=True)

class UserActivation(models.Model):
    # author = models.ForeignKey('User', unique=True, on_delete=models.CASCADE)
    active = models.BooleanField()
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(null=True)

class ResetPassword():
    # author = models.ForeignKey('User', unique=True, on_delete=models.CASCADE)
    active = models.BooleanField()
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(null=True)


