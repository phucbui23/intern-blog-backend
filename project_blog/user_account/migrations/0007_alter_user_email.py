# Generated by Django 4.0.5 on 2022-06-30 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_account', '0006_alter_user_active_alter_user_is_admin_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(default=1, max_length=255, unique=True),
            preserve_default=False,
        ),
    ]
