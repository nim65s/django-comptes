from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comptes', '0002_auto_20150517_2022'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dette',
            options={'ordering': ['-moment']},
        ),
        migrations.AlterModelOptions(
            name='remboursement',
            options={'ordering': ['-moment']},
        ),
    ]
