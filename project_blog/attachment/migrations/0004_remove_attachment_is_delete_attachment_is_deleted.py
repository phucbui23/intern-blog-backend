# Generated by Django 4.0.5 on 2022-07-04 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attachment', '0003_alter_attachment_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attachment',
            name='is_delete',
        ),
        migrations.AddField(
            model_name='attachment',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]