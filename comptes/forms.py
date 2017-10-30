from django import forms

from .models import Dette


class DetteForm(forms.ModelForm):
    class Meta:
        model = Dette
        fields = ['creancier', 'debiteurs', 'montant', 'description', 'date', 'time']
        widgets = {'debiteurs': forms.CheckboxSelectMultiple}
