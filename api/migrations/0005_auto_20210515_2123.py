# Generated by Django 3.1.6 on 2021-05-16 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_user_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matches',
            name='sport',
            field=models.CharField(choices=[('basketball', 'Basketball'), ('football', 'Football'), ('tennis', 'Tennis'), ('volleyball', 'VolleyBall'), ('frisbee', 'Frisbee')], max_length=15),
        ),
    ]
