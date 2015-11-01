from braces.views import UserPassesTestMixin

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.views.generic import CreateView

from .models import Dette, Occasion


@login_required
def home(request, slug=None):
    if slug is None:
        occasions = Occasion.objects.filter(clos=False).filter(Q(membres__isnull=True) | Q(membres=request.user))
    else:
        occasions = [get_object_or_404(Occasion, slug=slug)]
        if request.user not in occasions[0].get_membres():
            raise Http404
    return render(request, 'comptes/comptes.html', {'occasions': occasions})


class DetteCreateView(UserPassesTestMixin, CreateView):
    model = Dette
    fields = ['creancier', 'montant', 'debiteurs', 'description', 'moment']

    def test_func(self, user):
        self.occasion = get_object_or_404(Occasion, slug=self.kwargs['oc_slug'])
        return not self.occasion.membres.exists() is None or user in self.occasion.membres.all()

    def get_form(self, form_class=None):
        form = super(DetteCreateView, self).get_form(form_class)
        form.fields['creancier'].queryset = self.occasion.membres.all()
        form.fields['debiteurs'].queryset = self.occasion.membres.all()
        return form

    def form_valid(self, form):
        form.instance.occasion = self.occasion
        return super(DetteCreateView, self).form_valid(form)
