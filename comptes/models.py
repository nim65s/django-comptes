from datetime import time
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import (BooleanField, CharField, DateField, DateTimeField, DecimalField,
                              ForeignKey, ManyToManyField, Model, SlugField, Sum, TextField, TimeField)
from django.db.models.functions import Coalesce


def query_sum(queryset, field='montant'):
    return queryset.aggregate(s=Coalesce(Sum(field), 0))['s']


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
        return query_sum(self.dette_set)

    def solde(self, membre):
        solde = 0
        dettes = sum([d.montant / len(d.debiteurs.all()) for d in membre.dettes.filter(occasion=self)])
        creances = query_sum(self.dette_set.filter(creancier=membre))
        debits = query_sum(membre.debits.filter(occasion=self))
        credits = query_sum(membre.credits.filter(occasion=self))
        # debits2 = query_sum(self.remboursement_set.filter(crediteur=membre))
        # credits2 = query_sum(self.remboursement_set.filter(credite=membre))
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
    scribe = ForeignKey(User, related_name='+', null=True)
    cree = DateTimeField(auto_now_add=True)
    modifie = DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date", "-time"]

    def __str__(self):
        fmt = "Dette: %s a payé %.2f à %i personnes pour «%s»"
        return fmt % (self.creancier, self.montant, self.debiteurs.count(), self.description)

    def get_absolute_url(self):
        return self.occasion.get_absolute_url()

    def debiteurs_list(self):
        return ', '.join('%s' % debiteur for debiteur in self.debiteurs.all())


class Remboursement(Model):
    crediteur = ForeignKey(User, related_name='debits')
    credite = ForeignKey(User, related_name='credits')
    montant = DecimalField(max_digits=8, decimal_places=2)  # Je ne promet rien sur les dettes de 10M€ et plus
    date = DateField()
    time = TimeField('heure')
    occasion = ForeignKey(Occasion, null=True)
    scribe = ForeignKey(User, related_name='+', null=True)
    cree = DateTimeField(auto_now_add=True)
    modifie = DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date", "-time"]

    def __str__(self):
        return "%s a remboursé %.2f € à %s" % (self.crediteur, self.montant, self.credite)

    def get_absolute_url(self):
        return self.occasion.get_absolute_url()
