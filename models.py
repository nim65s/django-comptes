from datetime import time
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import (BooleanField, CharField, DateField, DateTimeField, DecimalField, ForeignKey, ManyToManyField, Model, SlugField, Sum, TextField,
                              TimeField)


class Occasion(Model):
    nom = CharField(max_length=50, unique=True)
    slug = SlugField(unique=True)
    description = TextField()
    membres = ManyToManyField(User, blank=True)
    debut = DateTimeField()
    fin = DateTimeField()
    clos = BooleanField(default=False)

    def __str__(self):
        return "Occasion: %s" % self.nom

    def get_absolute_url(self):
        return reverse('comptes:occasion', kwargs={'slug': self.slug})

    def get_membres(self):
        return self.membres.all() if self.membres.exists() else User.objects.all()

    def solde_des_membres(self):
        return sorted([(self.solde(m), m) for m in self.get_membres()], key=lambda x: x[0], reverse=True)

    def depenses(self):
        return self.dette_set.aggregate(s=Sum('montant'))['s']

    def solde(self, membre):
        solde = 0
        dettes = sum([d.montant / len(d.debiteurs.all()) for d in membre.dettes.filter(occasion=self)])
        creances = self.dette_set.filter(creancier=membre).aggregate(s=Sum('montant'))['s']
        debits = membre.debits.filter(occasion=self).aggregate(s=Sum('montant'))['s']
        credits = membre.credits.filter(occasion=self).aggregate(s=Sum('montant'))['s']
        # debits2 = self.remboursement_set.filter(crediteur=membre).aggregate(s=Sum('montant'))['s']
        # credits2 = self.remboursement_set.filter(credite=membre).aggregate(s=Sum('montant'))['s']
        if dettes:
            solde -= dettes
        if creances:
            solde += creances
        if debits:
            solde += debits
        if credits:
            solde -= credits

        return Decimal(solde).quantize(Decimal('.01'))


class Dette(Model):
    creancier = ForeignKey(User, related_name='creances')
    montant = DecimalField(max_digits=8, decimal_places=2)  # Je ne promet rien sur les dettes de 10M€ et plus
    debiteurs = ManyToManyField(User, related_name='dettes')
    description = TextField()
    date = DateField()
    time = TimeField('heure', default=time(12))
    occasion = ForeignKey(Occasion)

    def __str__(self):
        return "Dette: %s a payé %.2f à %i personnes pour «%s»" % (self.creancier, self.montant, self.debiteurs.count(), self.description)

    def get_absolute_url(self):
        return self.occasion.get_absolute_url()

    class Meta:
        ordering = ["-date", "-time"]


class Remboursement(Model):
    crediteur = ForeignKey(User, related_name='debits')
    credite = ForeignKey(User, related_name='credits')
    montant = DecimalField(max_digits=8, decimal_places=2)  # Je ne promet rien sur les dettes de 10M€ et plus
    moment = DateTimeField()
    occasion = ForeignKey(Occasion, null=True)

    def __str__(self):
        return "%s a remboursé %.2f € à %s" % (self.crediteur, self.montant, self.credite)

    class Meta:
        ordering = ["-moment"]
