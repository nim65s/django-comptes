# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('comptes', '0011_scribe'),
    ]

    operations = [
        migrations.AddField(
            model_name='dette',
            name='cree',
            field=models.DateTimeField(
                auto_now_add=True, default=datetime.datetime(2015, 11, 5, 6, 37, 24, 959875, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dette',
            name='modifie',
            field=models.DateTimeField(
                auto_now=True, default=datetime.datetime(2015, 11, 5, 6, 37, 29, 887492, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='remboursement',
            name='cree',
            field=models.DateTimeField(
                auto_now_add=True, default=datetime.datetime(2015, 11, 5, 6, 37, 34, 924435, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='remboursement',
            name='modifie',
            field=models.DateTimeField(
                auto_now=True, default=datetime.datetime(2015, 11, 5, 6, 37, 43, 246058, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
