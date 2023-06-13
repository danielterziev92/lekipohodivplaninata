# Generated by Django 4.2 on 2023-06-13 13:39

from django.db import migrations, models
import lekipohodivplaninata.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_alter_hikeevaluation_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hikeevaluation',
            name='assessment',
            field=models.PositiveSmallIntegerField(null=True, validators=[lekipohodivplaninata.core.validators.ValueInRangeValidator(1, 10)]),
        ),
    ]
