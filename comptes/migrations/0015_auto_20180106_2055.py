# Generated by Django 2.0.1 on 2018-01-06 20:55

from django.db import migrations


def rename(apps, schema_editor):
    Occasion = apps.get_model('comptes', 'Occasion')
    for occasion in Occasion.objects.all():
        occasion.name = occasion.nom
        occasion.save()


class Migration(migrations.Migration):

    dependencies = [
        ('comptes', '0014_auto_20180106_2054'),
    ]

    operations = [
        migrations.RunPython(rename),
    ]