# Generated by Django 4.2 on 2023-06-01 13:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hike', '0005_create_hike'),
    ]

    operations = [
        migrations.CreateModel(
            name='HikeAdditionalInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_venue', models.CharField(max_length=30)),
                ('departure_time', models.TimeField()),
                ('departure_place', models.CharField(max_length=30)),
                ('hike_id', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, to='hike.hike')),
            ],
        ),
    ]
