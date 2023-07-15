# Generated by Django 4.2 on 2023-06-03 15:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users_app', '0001_create_user_app'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseProfile',
            fields=[
                ('first_name', models.CharField(max_length=25, verbose_name='Име')),
                ('last_name', models.CharField(max_length=25, verbose_name='Фамилия')),
                ('phone_number', models.CharField(max_length=15)),
                ('user_id', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='Потребител')),
            ],
            options={
                'verbose_name_plural': 'Профили',
            },
        ),
    ]