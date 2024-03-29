# Generated by Django 4.2 on 2023-06-13 11:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hike', '0010_alter_hike_more_pictures'),
        ('users_app', '0005_remove_guideprofile_first_name_and_more'),
        ('base', '0003_create_site_evaluation'),
    ]

    operations = [
        migrations.AddField(
            model_name='signupforhike',
            name='is_confirmed',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='signupforhike',
            name='is_recommend',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='HikeEvaluationMoreInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hike_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hike.hike')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users_app.baseprofile')),
            ],
        ),
    ]
