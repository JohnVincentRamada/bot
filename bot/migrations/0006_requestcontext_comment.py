# Generated by Django 4.2.4 on 2023-11-10 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0005_requestcontext'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestcontext',
            name='comment',
            field=models.CharField(default=1, max_length=1000),
            preserve_default=False,
        ),
    ]
