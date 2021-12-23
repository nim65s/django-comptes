"""Models form Comptes."""

from decimal import Decimal
from typing import List, Tuple

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from ndh.models import Links, NamedModel, TimeStampedModel
from ndh.utils import query_sum


class Occasion(Links, NamedModel):
    """Define one occasion to share comptes with others."""

    description = models.TextField()
    membres = models.ManyToManyField(User, blank=True)
    debut = models.DateTimeField("début")
    fin = models.DateTimeField()
    clos = models.BooleanField(default=False)

    def get_absolute_url(self) -> str:
        """Get the url for the details view of this Occasion."""
        return reverse("comptes:occasion", kwargs={"slug": self.slug})

    def get_membres(self) -> models.QuerySet:
        """Get the list of members for this Occasion."""
        return self.membres.all() if self.membres.exists() else User.objects.all()

    def solde_des_membres(self) -> List[Tuple[Decimal, User]]:
        """Get a sorted list of membres with their balance for this Occasion."""
        return sorted(
            [(self.solde(m), m) for m in self.get_membres()], key=lambda x: -x[0]
        )

    def depenses(self) -> float:
        """Get the sum of all the money spend by everyone on this Occasion."""
        return query_sum(self.dette_set, "montant", output_field=models.DecimalField())

    def solde(self, membre: User) -> Decimal:
        """Get the balance of one member of this Occasion."""
        solde = Decimal(0)
        dettes = sum(
            [
                d.montant / len(d.debiteurs.all())
                for d in membre.dettes.filter(occasion=self)
            ]
        )
        creances = query_sum(
            self.dette_set.filter(creancier=membre),
            "montant",
            output_field=models.DecimalField(),
        )
        debits = query_sum(
            membre.debits.filter(occasion=self),
            "montant",
            output_field=models.DecimalField(),
        )
        credits = query_sum(
            membre.credits.filter(occasion=self),
            "montant",
            output_field=models.DecimalField(),
        )
        # debits2 = query_sum(self.remboursement_set.filter(crediteur=membre), 'montant',
        # output_field=models.DecimalField())
        # credits2 = query_sum(self.remboursement_set.filter(credite=membre), 'montant',
        # output_field=models.DecimalField())
        if dettes:
            solde -= dettes
        if creances:
            solde += creances
        if debits:
            solde += debits
        if credits:
            solde -= credits

        return Decimal(solde).quantize(Decimal(".01"))


class Dette(Links, TimeStampedModel):
    """Define a Dette between members of one particular Occasion."""

    creancier = models.ForeignKey(
        User,
        related_name="creances",
        verbose_name="créancier",
        on_delete=models.CASCADE,
    )
    montant = models.DecimalField(
        max_digits=8, decimal_places=2
    )  # Je ne promet rien sur les dettes de 10M€ et plus
    debiteurs = models.ManyToManyField(
        User, related_name="dettes", verbose_name="débiteurs"
    )
    description = models.TextField()
    moment = models.DateTimeField()
    occasion = models.ForeignKey(Occasion, on_delete=models.CASCADE)
    scribe = models.ForeignKey(
        User, related_name="+", null=True, on_delete=models.CASCADE
    )

    class Meta:
        """Meta."""

        ordering = ["-moment"]

    def __str__(self) -> str:
        """Describe this Dette."""
        return f"{self.creancier} a payé {self.montant:.2f} € à {self.debiteurs_list()} pour «{self.description}»"

    def get_absolute_url(self) -> str:
        """Return the url of the Occasion for this Dette."""
        return self.occasion.get_absolute_url()

    def debiteurs_list(self) -> str:
        """Get the list of debiteurs for this Dette as a string."""
        # This method does not work when there are no debiteurs. Duh.
        debiteurs = list(self.debiteurs.values_list("username", flat=True))
        if len(debiteurs) == 1:
            return debiteurs[0]
        return ", ".join(debiteurs[:-1]) + " & " + debiteurs[-1]

    def part(self) -> Decimal:
        """Return the amount of this Dette devided equally between its debiteurs."""
        return self.montant / self.debiteurs.count()


class Remboursement(Links, TimeStampedModel):
    """Define a Remboursement between members for one Occasion."""

    crediteur = models.ForeignKey(
        User, related_name="debits", verbose_name="créditeur", on_delete=models.CASCADE
    )
    credite = models.ForeignKey(
        User, related_name="credits", verbose_name="crédité", on_delete=models.CASCADE
    )
    montant = models.DecimalField(
        max_digits=8, decimal_places=2
    )  # Je ne promet rien sur les dettes de 10M€ et plus
    moment = models.DateTimeField()
    occasion = models.ForeignKey(Occasion, null=True, on_delete=models.CASCADE)
    scribe = models.ForeignKey(
        User, related_name="+", null=True, on_delete=models.CASCADE
    )

    class Meta:
        """Meta."""

        ordering = ["-moment"]

    def __str__(self) -> str:
        """Describe this Remboursement."""
        return f"{self.crediteur} a remboursé {self.montant:.2f} € à {self.credite}"

    def get_absolute_url(self):
        """Return the url of the Occasion for this Dette."""
        return self.occasion.get_absolute_url()
