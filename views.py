from braces.views import UserPassesTestMixin

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.views.generic import CreateView

from .models import Dette, Occasion, Remboursement


@login_required
def home(request, slug=None):
    if slug is None:
        occasions = Occasion.objects.filter(clos=False).filter(Q(membres__isnull=True) | Q(membres=request.user))
    else:
        occasions = [get_object_or_404(Occasion, slug=slug)]
        if request.user not in occasions[0].get_membres():
            raise Http404
    return render(request, 'comptes/comptes.html', {'occasions': occasions})


class DetteOrRemboursementCreateView(UserPassesTestMixin, CreateView):
    def test_func(self, user):
        self.occasion = get_object_or_404(Occasion, slug=self.kwargs['oc_slug'])
        return not self.occasion.membres.exists() or user in self.occasion.membres.all()

    def get_form(self, form_class=None):
        form = super(DetteOrRemboursementCreateView, self).get_form(form_class)
        for membres in self.fields[:2]:
            form.fields[membres].queryset = self.occasion.membres.all()
        return form

    def form_valid(self, form):
        form.instance.occasion = self.occasion
        return super(DetteOrRemboursementCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super(DetteOrRemboursementCreateView, self).get_context_data(**kwargs)
        ctx['occasion'] = self.occasion
        return ctx


class DetteCreateView(DetteOrRemboursementCreateView):
    model = Dette
    fields = ['creancier', 'debiteurs', 'montant', 'description', 'date', 'time']


class RemboursementCreateView(DetteOrRemboursementCreateView):
    model = Remboursement
    fields = ['crediteur', 'credite', 'montant', 'date', 'time']
