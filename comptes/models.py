from datetime import time
from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models
from django.db.models import (BooleanField, DateField, DateTimeField, DecimalField,
                              ForeignKey, ManyToManyField, Model, TextField, TimeField)
from django.urls import reverse

from ndh.models import Links, NamedModel
from ndh.utils import query_sum


class Occasion(Links, NamedModel):
    description = TextField()
    membres = ManyToManyField(User, blank=True)
    debut = DateTimeField('début')
    fin = DateTimeField()
    clos = BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('comptes:occasion', kwargs={'slug': self.slug})

    def get_membres(self):
        return self.membres.all() if self.membres.exists() else User.objects.all()

    def solde_des_membres(self):
        return sorted([(self.solde(m), m) for m in self.get_membres()], key=lambda x: -x[0])

    def depenses(self):
        return query_sum(self.dette_set, 'montant')

    def solde(self, membre):
        solde = 0
        dettes = sum([d.montant / len(d.debiteurs.all()) for d in membre.dettes.filter(occasion=self)])
        creances = query_sum(self.dette_set.filter(creancier=membre), 'montant')
        debits = query_sum(membre.debits.filter(occasion=self), 'montant')
        credits = query_sum(membre.credits.filter(occasion=self), 'montant')
        # debits2 = query_sum(self.remboursement_set.filter(crediteur=membre), 'montant')
        # credits2 = query_sum(self.remboursement_set.filter(credite=membre), 'montant')
        if dettes:
            solde -= dettes
        if creances:
            solde += creances
        if debits:
            solde += debits
        if credits:
            solde -= credits

        return Decimal(solde).quantize(Decimal('.01'))


class Dette(Links, Model):
    creancier = ForeignKey(User, related_name='creances', verbose_name='créancier', on_delete=models.CASCADE)
    montant = DecimalField(max_digits=8, decimal_places=2)  # Je ne promet rien sur les dettes de 10M€ et plus
    debiteurs = ManyToManyField(User, related_name='dettes', verbose_name='débiteurs')
    description = TextField()
    date = DateField()
    time = TimeField('heure', default=time(12))
    occasion = ForeignKey(Occasion, on_delete=models.CASCADE)
    scribe = ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    cree = DateTimeField('créé', auto_now_add=True)
    modifie = DateTimeField('modifié', auto_now=True)

    class Meta:
        ordering = ["-date", "-time"]

    def __str__(self):
        fmt = "Dette: %s a payé %.2f à %i personnes pour «%s»"
        return fmt % (self.creancier, self.montant, self.debiteurs.count(), self.description)

    def get_absolute_url(self):
        return self.occasion.get_absolute_url()

    def debiteurs_list(self):
        # This method does not work when there are no debiteurs. Duh.
        debiteurs = list(self.debiteurs.values_list('username', flat=True))
        if len(debiteurs) == 1:
            return debiteurs[0]
        return ', '.join(debiteurs[:-1]) + ' & ' + debiteurs[-1]

    def part(self):
        return self.montant / self.debiteurs.count()


class Remboursement(Links, Model):
    crediteur = ForeignKey(User, related_name='debits', verbose_name='créditeur', on_delete=models.CASCADE)
    credite = ForeignKey(User, related_name='credits', verbose_name='crédité', on_delete=models.CASCADE)
    montant = DecimalField(max_digits=8, decimal_places=2)  # Je ne promet rien sur les dettes de 10M€ et plus
    date = DateField()
    time = TimeField('heure')
    occasion = ForeignKey(Occasion, null=True, on_delete=models.CASCADE)
    scribe = ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    cree = DateTimeField('créé', auto_now_add=True)
    modifie = DateTimeField('modifié', auto_now=True)

    class Meta:
        ordering = ["-date", "-time"]

    def __str__(self):
        return "%s a remboursé %.2f € à %s" % (self.crediteur, self.montant, self.credite)

    def get_absolute_url(self):
        return self.occasion.get_absolute_url()
