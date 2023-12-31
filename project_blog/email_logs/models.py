from django.db import models
from utils.enums import Type
from user_account.models import User
# Create your models here.


class EmailLogs(models.Model):
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        to_field='id',
        related_name='email_logs_fk_author',
        db_column='author_id',
        db_constraint=False,
        null=False,
        blank=False,
    )
    type = models.TextField(
        choices=Type.choices, 
        default=Type.ACTIVATE,
    )
    subject = models.TextField()
    content = models.TextField()
    is_success = models.BooleanField(default=False)
    sended_at = models.DateTimeField(
        auto_now=True, 
        null=True, 
        blank=True,
    )

    @staticmethod
    def send_follower_email(followers, subject, body):
        for follower in followers:
            EmailLogs.objects.create(
                author=follower.follower,
                type=Type.FOLLOWER_POST,
                is_success=True,
                subject=subject,
                content=body,
            )


    def __str__(self) -> str:
        return f'{self.author.email} -> {self.type}'
        