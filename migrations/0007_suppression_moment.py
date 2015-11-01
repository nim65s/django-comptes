# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comptes', '0006_moment_to_date_time'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dette',
            options={'ordering': ['-date', '-time']},
        ),
        migrations.RemoveField(
            model_name='dette',
            name='moment',
        ),
        migrations.AlterField(
            model_name='dette',
            name='time',
            field=models.TimeField(verbose_name='heure'),
        ),
    ]
