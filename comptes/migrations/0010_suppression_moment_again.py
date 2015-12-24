# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comptes', '0009_moment_to_date_time_again'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='remboursement',
            options={'ordering': ['-date', '-time']},
        ),
        migrations.RemoveField(
            model_name='remboursement',
            name='moment',
        ),
    ]
