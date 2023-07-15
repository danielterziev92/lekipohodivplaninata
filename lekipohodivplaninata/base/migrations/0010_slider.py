# Generated by Django 4.2 on 2023-07-15 13:01

import cloudinary.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hike', '0010_alter_hike_more_pictures'),
        ('base', '0009_hikeevaluationusers_remove_hikeevaluation_more_info_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', cloudinary.models.CloudinaryField(help_text='Тук трябва добавите основна снимка за похода', max_length=255, verbose_name='нимка')),
                ('hike_id', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, to='hike.hike')),
            ],
        ),
    ]