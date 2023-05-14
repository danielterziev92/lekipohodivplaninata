# Generated by Django 4.2 on 2023-05-14 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_app', '0004_guideprofile'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='baseprofile',
            options={'verbose_name': 'име и фамилия', 'verbose_name_plural': 'Профили'},
        ),
        migrations.AlterModelOptions(
            name='guideprofile',
            options={'verbose_name': 'прифила на водач', 'verbose_name_plural': 'Водачи'},
        ),
        migrations.AlterModelOptions(
            name='userapp',
            options={'verbose_name': 'потребител', 'verbose_name_plural': 'Потребители'},
        ),
        migrations.AlterField(
            model_name='userapp',
            name='email',
            field=models.EmailField(error_messages={'unique': 'Моля използвайте по-сложна парола.'}, max_length=254, unique=True, verbose_name='Имейл'),
        ),
    ]
