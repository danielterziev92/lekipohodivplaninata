# Generated by Django 4.2 on 2023-06-01 14:33

import cloudinary.models
from django.db import migrations, models
import django.db.models.deletion
import lekipohodivplaninata.hike.validators


class Migration(migrations.Migration):

    dependencies = [
        ('hike', '0004_create_hike_more_pictures'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateField(auto_now_add=True)),
                ('updated_on', models.DateField(auto_now=True)),
                ('title', models.CharField(help_text='Моля попълнете заглавие на похода', max_length=30, verbose_name='Заглавие')),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('description', models.TextField(help_text='Моля попълнете описание за похода', verbose_name='Описание')),
                ('duration', models.CharField(help_text='Моля попълнете продължителността на похода в цифри', max_length=20, verbose_name='Продължителност')),
                ('event_date', models.DateField(help_text='Моля изберете дата за похода', validators=[lekipohodivplaninata.hike.validators.BeforeTodayValidator], verbose_name='Дата на похода')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, help_text='Моля попълнете само цифрата на сумата за похода', max_digits=8, verbose_name='Цена')),
                ('main_picture', cloudinary.models.CloudinaryField(help_text='Тук трябва добавите основна снимка за похода', max_length=255, verbose_name='Основна снимка')),
                ('level', models.ForeignKey(help_text='Моля изберете ниво за похода', on_delete=django.db.models.deletion.RESTRICT, to='hike.hikelevel', verbose_name='Ниво на похода')),
                ('more_pictures', models.ManyToManyField(blank=True, help_text='Тук можете да добавите допълнителни снимки за похода', null=True, to='hike.hikemorepicture', verbose_name='Допълнителни снимки')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='hike.hiketype')),
            ],
            options={
                'verbose_name': 'поход',
                'verbose_name_plural': 'Походи',
            },
        ),
    ]
