# Generated by Django 4.2 on 2023-05-27 21:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users_app', '0002_create_app_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseProfile',
            fields=[
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='Потребител')),
                ('first_name', models.CharField(max_length=25, verbose_name='Име')),
                ('last_name', models.CharField(max_length=25, verbose_name='Фамилия')),
            ],
            options={
                'verbose_name': 'име и фамилия',
                'verbose_name_plural': 'Профили',
            },
        ),
    ]