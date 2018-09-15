from django.db import migrations, models


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
        migrations.DeleteModel(name='Couple', ),
    ]
