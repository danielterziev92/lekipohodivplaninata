# Generated by Django 4.2 on 2023-06-13 11:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('base', '0006_add_and_remove_slug_hike_evaluation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hikeevaluation',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
            preserve_default=False,
        ),
    ]
