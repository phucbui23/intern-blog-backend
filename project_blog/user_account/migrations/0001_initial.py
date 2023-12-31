# Generated by Django 4.0.5 on 2022-06-27 07:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('email', models.CharField(blank=True, max_length=255, null=True)),
                ('phone_number', models.CharField(max_length=16, null=True)),
                ('full_name', models.CharField(max_length=255, null=True)),
                ('nick_name', models.CharField(max_length=255, null=True)),
                ('quote', models.TextField(null=True)),
                ('gender', models.CharField(choices=[('MALE', 'Male'), ('FEMALE', 'Female'), ('OTHER', 'Other')], default='OTHER', max_length=12, null=True)),
                ('status', models.CharField(max_length=16)),
                ('active', models.BooleanField()),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('is_superuser', models.BooleanField()),
                ('is_admin', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Follower',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField()),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField(null=True)),
                ('author', models.ForeignKey(db_column='author_id', db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='follower_fk_author', to='user_account.user')),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower_fk_follower', to='user_account.user')),
            ],
        ),
    ]
