# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comptes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='couple',
            name='femme',
        ),
        migrations.RemoveField(
            model_name='couple',
            name='mari',
        ),
        migrations.RemoveField(
            model_name='occasion',
            name='couples_membres',
        ),
        migrations.DeleteModel(
            name='Couple',
        ),
    ]
