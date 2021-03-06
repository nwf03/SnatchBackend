# Generated by Django 3.1.6 on 2021-07-02 02:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20210616_1454'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_name', models.CharField(max_length=100)),
                ('location_address', models.CharField(max_length=300)),
                ('location_city', models.CharField(max_length=100)),
                ('location_state', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='matches',
            name='location_address',
        ),
        migrations.RemoveField(
            model_name='matches',
            name='location_city_state',
        ),
        migrations.RemoveField(
            model_name='matches',
            name='location_name',
        ),
        migrations.AddField(
            model_name='matches',
            name='match_location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='location', to='api.location'),
        ),
    ]
