# Generated by Django 3.1.6 on 2021-05-13 11:20

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20210513_0617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matches',
            name='challenger',
            field=models.ManyToManyField(blank=True, null=True, related_name='challenger', to=settings.AUTH_USER_MODEL),
        ),
    ]
