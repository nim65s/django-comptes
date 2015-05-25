# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from decimal import Decimal

from django.contrib.auth.models import User
from django.db.models import BooleanField, CharField, DateTimeField, DecimalField, ForeignKey, ManyToManyField, Model, SlugField, Sum, TextField
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Occasion(Model):
    nom = CharField(max_length=50, unique=True)
    slug = SlugField(unique=True)
    description = TextField()
    membres = ManyToManyField(User)
    debut = DateTimeField()
    fin = DateTimeField()
    clos = BooleanField(default=False)

    def __str__(self):
        return "Occasion: %s" % self.nom

    def solde_des_membres(self):
        return sorted([(self.solde(m), m) for m in self.membres.all()], reverse=True)

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


@python_2_unicode_compatible
class Dette(Model):
    creancier = ForeignKey(User, related_name='creances')
    montant = DecimalField(max_digits=8, decimal_places=2)  # Je ne promet rien sur les dettes de 10M€ et plus
    debiteurs = ManyToManyField(User, related_name='dettes')
    description = TextField()
    moment = DateTimeField()
    occasion = ForeignKey(Occasion)

    def __str__(self):
        return "Dette: %s a payé %.2f à %i personnes pour «%s»" % (self.creancier, self.montant, len(self.debiteurs.all()), self.description)

    class Meta:
        ordering = ["-moment"]


@python_2_unicode_compatible
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
