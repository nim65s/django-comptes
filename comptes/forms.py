"""Forms for Comptes."""
from django import forms

from ndh.forms import AccessibleDateTimeField

from .models import Dette, Remboursement


class DetteForm(forms.ModelForm):
    """ModelForm for Dettes."""

    moment = AccessibleDateTimeField()

    class Meta:
        """Meta."""

        model = Dette
        fields = ["creancier", "debiteurs", "montant", "description", "moment"]
        widgets = {"debiteurs": forms.CheckboxSelectMultiple}


class RemboursementForm(forms.ModelForm):
    """ModelForm for Remboursements."""

    moment = AccessibleDateTimeField()

    class Meta:
        """Meta."""

        model = Remboursement
        fields = ["crediteur", "credite", "montant", "moment"]
