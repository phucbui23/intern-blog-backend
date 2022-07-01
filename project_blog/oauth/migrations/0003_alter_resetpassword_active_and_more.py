# Generated by Django 4.0.5 on 2022-07-01 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oauth', '0002_resetpassword'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resetpassword',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='useractivation',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='userdevicetoken',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='userdevicetoken',
            name='device_model',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
