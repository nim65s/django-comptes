# Generated by Django 2.0.1 on 2018-01-06 20:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comptes', '0015_auto_20180106_2055'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='occasion',
            name='nom',
        ),
    ]
