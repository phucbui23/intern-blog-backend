from django.db import models

# Create your models here.


class EmailLogs(models.Model):
    TYPE_VALUES = [
        ('ACTIVATE', 'ACTIVATE'), 
        ('RESET_PASSWORD','RESET_PASSWORD'), 
        ('FOLLOWER_POST', 'FOLLOWER_POST'),
    ]
    # author = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.TextField(choices=TYPE_VALUES)
    subject = models.TextField()
    content = models.TextField()
    is_success = models.BooleanField()
    sended_at = models.DateTimeField(null=True)
