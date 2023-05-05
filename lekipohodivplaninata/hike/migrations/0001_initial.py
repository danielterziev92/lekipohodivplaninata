# Generated by Django 4.2 on 2023-05-05 08:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HikeLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Моля попълнете вида трудност', max_length=30, verbose_name='Заглавие')),
            ],
        ),
        migrations.CreateModel(
            name='HikeMorePicture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(upload_to='hikes-more-pictures')),
            ],
        ),
        migrations.CreateModel(
            name='HikeType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Моля попълнете типа на похода', max_length=30, verbose_name='Заглавие')),
            ],
        ),
        migrations.CreateModel(
            name='Hike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateField(auto_now_add=True)),
                ('updated_on', models.DateField(auto_now=True)),
                ('title', models.CharField(help_text='Моля попълнете заглавие на похода', max_length=30, verbose_name='Заглавие')),
                ('description', models.TextField(help_text='Моля попълнете описание за похода', verbose_name='Описание')),
                ('duration', models.CharField(help_text='Моля попълнете продължителността на похода', max_length=20, verbose_name='Продължителност')),
                ('event_date', models.DateField()),
                ('price', models.DecimalField(decimal_places=2, help_text='Моля попълнете само цифрата на сумата за похода', max_digits=8, verbose_name='Цена')),
                ('main_picture', models.ImageField(upload_to='hike-main-pictures')),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='hike.hikelevel')),
                ('more_pictures', models.ManyToManyField(to='hike.hikemorepicture')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
