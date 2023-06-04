# Generated by Django 4.2 on 2023-06-03 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_app', '0004_create_guide_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnonymousAppUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=25, verbose_name='Име')),
                ('last_name', models.CharField(max_length=25, verbose_name='Фамилия')),
                ('phone_number', models.CharField(max_length=15)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
