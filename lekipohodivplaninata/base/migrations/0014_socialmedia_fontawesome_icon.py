# Generated by Django 4.2 on 2023-07-16 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_settings'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialmedia',
            name='fontawesome_icon',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
