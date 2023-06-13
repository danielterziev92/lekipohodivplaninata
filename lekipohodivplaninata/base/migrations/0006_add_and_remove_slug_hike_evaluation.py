
from django.db import migrations
from django.utils.text import slugify

from lekipohodivplaninata.core.mixins import CommonMixin


def add_slugs(apps, schema_editor):
    HikeEvaluation = apps.get_model('base', 'HikeEvaluation')

    objects = HikeEvaluation.objects.all()

    for obj in objects:
        obj.slug = slugify(CommonMixin.generate_random_string(20))

    HikeEvaluation.objects.bulk_update(objects, fields=['slug'])


def delete_slugs(apps, schema_editor):
    HikeEvaluation = apps.get_model('base', 'HikeEvaluation')

    objects = HikeEvaluation.objects.all()

    for obj in objects:
        obj.slug = None

    HikeEvaluation.objects.bulk_update(objects, fields=['slug'])


class Migration(migrations.Migration):
    dependencies = [
        ('base', '0005_hikeevaluation'),
    ]

    operations = [
        migrations.RunPython(add_slugs, delete_slugs)
    ]
