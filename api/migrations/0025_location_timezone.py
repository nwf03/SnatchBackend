# Generated by Django 3.1.6 on 2021-08-14 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_auto_20210803_2224'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='timezone',
            field=models.CharField(default='', max_length=50),
        ),
    ]
