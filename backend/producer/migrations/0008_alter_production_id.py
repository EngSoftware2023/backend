# Generated by Django 4.2.6 on 2023-10-21 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producer', '0007_alter_production_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='production',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]