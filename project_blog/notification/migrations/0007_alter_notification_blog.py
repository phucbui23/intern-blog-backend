# Generated by Django 4.0.5 on 2022-07-12 14:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_alter_blog_author'),
        ('notification', '0006_alter_notification_blog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='blog',
            field=models.ForeignKey(db_column='blog_uid', on_delete=django.db.models.deletion.CASCADE, related_name='notification_fk_blog', to='blog.blog'),
        ),
    ]
