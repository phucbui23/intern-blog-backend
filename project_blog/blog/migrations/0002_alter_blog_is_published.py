# Generated by Django 4.0.5 on 2022-07-04 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='is_published',
            field=models.BooleanField(default=False),
        ),
    ]
