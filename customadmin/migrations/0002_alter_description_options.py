# Generated by Django 4.2.4 on 2023-11-20 13:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customadmin', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='description',
            options={'ordering': ('-created_at',)},
        ),
    ]