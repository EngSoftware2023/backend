# Generated by Django 4.2.6 on 2023-10-27 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producer', '0009_alter_production_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='production',
            name='price',
        ),
        migrations.AddField(
            model_name='production',
            name='status',
            field=models.CharField(default='Disponível', max_length=50),
        ),
    ]