# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('comptes', '0004_auto_20150921_1254'),
    ]

    operations = [
        migrations.AddField(
            model_name='dette',
            name='date',
            field=models.DateField(default=datetime.datetime(2015, 11, 1, 11, 54, 36, 726308, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dette',
            name='time',
            field=models.TimeField(default=datetime.datetime(2015, 11, 1, 11, 54, 47, 434082, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
