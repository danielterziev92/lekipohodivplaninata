# Generated by Django 4.2.3 on 2023-08-12 21:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users_app', '0005_remove_guideprofile_first_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseprofile',
            name='user_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='Потребител'),
        ),
        migrations.AlterField(
            model_name='guideprofile',
            name='user_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='Потребител'),
        ),
    ]