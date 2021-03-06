# Generated by Django 3.1.6 on 2021-06-16 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20210608_1104'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='matches',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='matches',
            name='longitude',
        ),
        migrations.AddField(
            model_name='matches',
            name='location_address',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='matches',
            name='location_city_state',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='matches',
            name='location_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
