# Generated by Django 4.2.6 on 2023-10-27 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='time_life',
            field=models.IntegerField(default=1),
        ),
    ]
