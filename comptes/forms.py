from django import forms

from ndh.forms import AccessibleDateTimeField

from .models import Dette, Remboursement


class DetteForm(forms.ModelForm):
    moment = AccessibleDateTimeField()

    class Meta:
        model = Dette
        fields = ['creancier', 'debiteurs', 'montant', 'description', 'moment']
        widgets = {'debiteurs': forms.CheckboxSelectMultiple}


class RemboursementForm(forms.ModelForm):
    moment = AccessibleDateTimeField()

    class Meta:
        model = Remboursement
        fields = ['crediteur', 'credite', 'montant', 'moment']
