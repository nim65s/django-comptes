# Generated by Django 2.0.1 on 2018-01-06 21:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comptes', '0017_auto_20180106_2110'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dette',
            old_name='cree',
            new_name='created',
        ),
        migrations.RenameField(
            model_name='dette',
            old_name='modifie',
            new_name='updated',
        ),
        migrations.RenameField(
            model_name='remboursement',
            old_name='cree',
            new_name='created',
        ),
        migrations.RenameField(
            model_name='remboursement',
            old_name='modifie',
            new_name='updated',
        ),
    ]