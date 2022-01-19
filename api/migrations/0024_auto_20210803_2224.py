# Generated by Django 3.1.6 on 2021-08-04 03:24

import api.models
from django.db import migrations, models
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_auto_20210730_2220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='age',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='user',
            name='location_city',
            field=models.CharField(default='Bloomington', max_length=70),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='location_state',
            field=models.CharField(default='Indiana', max_length=70),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='user_picture',
            field=image_cropping.fields.ImageCropField(upload_to=api.models.User.upload_to),
        ),
        migrations.AlterField(
            model_name='user',
            name='weight',
            field=models.IntegerField(),
        ),
    ]