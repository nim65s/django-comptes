from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
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
            raise PermissionDenied
    return render(request, 'comptes/comptes.html', {'occasions': occasions})


class DetteOrRemboursementCreateView(UserPassesTestMixin, CreateView):
    def test_func(self):
        self.occasion = get_object_or_404(Occasion, slug=self.kwargs['oc_slug'])
        return not self.occasion.membres.exists() or self.request.user in self.occasion.membres.all()

    def get_form(self, form_class=None):
        form = super(DetteOrRemboursementCreateView, self).get_form(form_class)
        if self.occasion.membres.exists():
            for membres in self.fields[:2]:
                form.fields[membres].queryset = self.occasion.membres.all()
        return form

    def form_valid(self, form):
        form.instance.occasion = self.occasion
        form.instance.scribe = self.request.user
        return super(DetteOrRemboursementCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super(DetteOrRemboursementCreateView, self).get_context_data(**kwargs)
        ctx['occasion'] = self.occasion
        return ctx

    def get_success_url(self):
        if 'add_another' in self.request.POST:
            return self.request.path
        return super(DetteOrRemboursementCreateView, self).get_success_url()


class DetteCreateView(DetteOrRemboursementCreateView):
    model = Dette
    fields = ['creancier', 'debiteurs', 'montant', 'description', 'date', 'time']


class RemboursementCreateView(DetteOrRemboursementCreateView):
    model = Remboursement
    fields = ['crediteur', 'credite', 'montant', 'date', 'time']
