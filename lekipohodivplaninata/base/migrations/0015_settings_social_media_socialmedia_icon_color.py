# Generated by Django 4.2 on 2023-07-16 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_socialmedia_fontawesome_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='social_media',
            field=models.ManyToManyField(blank=True, null=True, to='base.socialmedia'),
        ),
        migrations.AddField(
            model_name='socialmedia',
            name='icon_color',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]