from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Couple',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('femme', models.ForeignKey(
                    on_delete=models.CASCADE, related_name='femme', to=settings.AUTH_USER_MODEL)),
                ('mari', models.ForeignKey(on_delete=models.CASCADE, related_name='mari',
                                           to=settings.AUTH_USER_MODEL)),
            ],
            options={},
            bases=(models.Model, ),
        ),
        migrations.CreateModel(
            name='Dette',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('montant', models.DecimalField(max_digits=8, decimal_places=2)),
                ('description', models.TextField()),
                ('moment', models.DateTimeField()),
                ('creancier',
                 models.ForeignKey(on_delete=models.CASCADE, related_name='creances', to=settings.AUTH_USER_MODEL)),
                ('debiteurs', models.ManyToManyField(related_name='dettes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['moment'],
            },
            bases=(models.Model, ),
        ),
        migrations.CreateModel(
            name='Occasion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(unique=True, max_length=50)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField()),
                ('debut', models.DateTimeField()),
                ('fin', models.DateTimeField()),
                ('clos', models.BooleanField(default=False)),
                ('couples_membres', models.ManyToManyField(to='comptes.Couple', blank=True)),
                ('membres', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={},
            bases=(models.Model, ),
        ),
        migrations.CreateModel(
            name='Remboursement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('montant', models.DecimalField(max_digits=8, decimal_places=2)),
                ('moment', models.DateTimeField()),
                ('credite',
                 models.ForeignKey(on_delete=models.CASCADE, related_name='credits', to=settings.AUTH_USER_MODEL)),
                ('crediteur',
                 models.ForeignKey(on_delete=models.CASCADE, related_name='debits', to=settings.AUTH_USER_MODEL)),
                ('occasion', models.ForeignKey(on_delete=models.CASCADE, to='comptes.Occasion', null=True)),
            ],
            options={
                'ordering': ['moment'],
            },
            bases=(models.Model, ),
        ),
        migrations.AddField(
            model_name='dette',
            name='occasion',
            field=models.ForeignKey(on_delete=models.CASCADE, to='comptes.Occasion'),
            preserve_default=True,
        ),
    ]
