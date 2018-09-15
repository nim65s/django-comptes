# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def moment_to_date_time(apps, schema_editor):
    Dette = apps.get_model('comptes', 'Remboursement')  # c/c
    for dette in Dette.objects.all():
        dette.date = dette.moment.date()
        dette.time = dette.moment.time()
        dette.save()


class Migration(migrations.Migration):

    dependencies = [
        ('comptes', '0008_add_date_time_fields_again'),
    ]

    operations = [
        migrations.RunPython(moment_to_date_time),
    ]
