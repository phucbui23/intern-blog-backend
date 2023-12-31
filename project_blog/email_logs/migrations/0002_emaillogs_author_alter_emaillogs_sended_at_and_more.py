# Generated by Django 4.0.5 on 2022-06-27 09:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_account', '0001_initial'),
        ('email_logs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='emaillogs',
            name='author',
            field=models.ForeignKey(db_column='author_id', db_constraint=False, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='email_logs_fk_author', to='user_account.user'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='emaillogs',
            name='sended_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='emaillogs',
            name='type',
            field=models.TextField(choices=[('ACTIVATE', 'Activate'), ('RESET_PASSWORD', 'Reset Password'), ('FOLLOWER_POST', 'Follower Post')], default='ACTIVATE'),
        ),
    ]
