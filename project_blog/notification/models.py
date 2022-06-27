from django.db import models

# Create your models here.
class Notification(models.Model):
    type = models.TextField()
    subject = models.TextField()
    content = models.TextField()
    is_success = models.BooleanField()
    sended_at = models.DateTimeField(null=True)
    # author = models.ForeignKey('User', on_delete=models.CASCADE)
    is_seen = models.BooleanField()