# Generated by Django 4.2 on 2023-06-03 15:13

import cloudinary.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users_app', '0002_create_base_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='GuideProfile',
            fields=[
                ('first_name', models.CharField(max_length=25, verbose_name='Име')),
                ('last_name', models.CharField(max_length=25, verbose_name='Фамилия')),
                ('user_id', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='Потребител')),
                ('avatar', cloudinary.models.CloudinaryField(max_length=255, verbose_name='Профилна снимка')),
                ('date_of_birth', models.DateField(verbose_name='Дата на раждане')),
                ('description', models.TextField(verbose_name='Описание')),
                ('certificate', cloudinary.models.CloudinaryField(max_length=255, verbose_name='Сертификат')),
                ('profile_id', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, to='users_app.baseprofile', verbose_name='Профил')),
            ],
            options={
                'verbose_name_plural': 'Водачи',
            },
        ),
    ]