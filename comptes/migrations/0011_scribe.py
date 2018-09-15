# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('comptes', '0010_suppression_moment_again'),
    ]

    operations = [
        migrations.AddField(
            model_name='dette',
            name='scribe',
            field=models.ForeignKey(
                on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL, null=True, related_name='+'),
        ),
        migrations.AddField(
            model_name='remboursement',
            name='scribe',
            field=models.ForeignKey(
                on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL, null=True, related_name='+'),
        ),
    ]
