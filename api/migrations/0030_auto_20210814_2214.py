# Generated by Django 3.1.6 on 2021-08-15 03:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0029_location_timezone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='location',
            name='longitude',
        ),
    ]
