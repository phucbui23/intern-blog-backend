from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attachment', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attachment',
            name='id',
        ),
        migrations.AlterField(
            model_name='attachment',
            name='uid',
            field=models.CharField(editable=False, max_length=36, primary_key=True, serialize=False, unique=True),
        ),
    ]
