# Generated by Django 4.2.6 on 2023-11-12 23:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_user_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
    ]
