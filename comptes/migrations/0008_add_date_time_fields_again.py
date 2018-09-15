# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('comptes', '0007_suppression_moment'),
    ]

    operations = [
        migrations.AddField(
            model_name='remboursement',
            name='date',
            field=models.DateField(default=datetime.datetime(2015, 11, 1, 12, 35, 21, 707065, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='remboursement',
            name='time',
            field=models.TimeField(
                default=datetime.datetime(2015, 11, 1, 12, 35, 25, 529116, tzinfo=utc), verbose_name='heure'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='dette',
            name='time',
            field=models.TimeField(default=datetime.time(12, 0), verbose_name='heure'),
        ),
    ]
