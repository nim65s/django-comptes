"""Views for comptes."""

from typing import Optional

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic import CreateView

from dmdm.mail import send_mail

from .forms import DetteForm, RemboursementForm
from .models import Dette, Occasion, Remboursement


@login_required
def home(request: HttpRequest, slug: Optional[str] = None) -> HttpResponse:
    """List the Occasions the user is in, or show one particular Occasion."""
    if slug is None:
        occasions = Occasion.objects.filter(clos=False).filter(
            Q(membres__isnull=True) | Q(membres=request.user)
        )
        soldes = sorted(
            [(sum(o.solde(m) for o in occasions), m) for m in User.objects.all()],
            key=lambda x: -x[0],
        )
        return render(
            request,
            "comptes/occasion_list.html",
            {"occasions": occasions, "soldes": soldes},
        )
    occasion = get_object_or_404(Occasion, slug=slug)
    if request.user not in occasion.get_membres():
        raise PermissionDenied
    return render(request, "comptes/occasion_detail.html", {"occasion": occasion})


class DetteOrRemboursementCreateView(UserPassesTestMixin, CreateView):
    """Mixin to for model create views."""

    def test_func(self):
        """Check that a user has access to the requested Occasion."""
        if not self.request.user.is_authenticated:
            return False
        self.occasion = get_object_or_404(Occasion, slug=self.kwargs["oc_slug"])
        return (
            not self.occasion.membres.exists()
            or self.request.user in self.occasion.membres.all()
        )

    def get_form(self, form_class=None):
        """Order members of the Occasion by their username."""
        form = super(DetteOrRemboursementCreateView, self).get_form(form_class)
        if self.occasion.membres.exists():
            fields = self.fields or self.form_class.Meta.fields
            for membres in fields[:2]:
                form.fields[membres].queryset = self.occasion.membres.order_by(
                    "username"
                )
        return form

    def form_valid(self, form):
        """Validate form on success, and send mail."""
        form.instance.occasion = self.occasion
        form.instance.scribe = self.request.user
        self.object = form.save()
        if not settings.DEBUG:
            self.send_mail()
        return HttpResponseRedirect(self.get_success_url())

    def send_mail(self):
        """Send a mail describing the last additions to all concerned members."""
        model = self.model.__name__
        ctx = {"object": self.object}
        subject = f"{model} ajouté"
        emails = []
        if model == "Remboursement":
            if self.object.crediteur.email:
                emails.append(self.object.crediteur.email)
            if self.object.credite.email:
                emails.append(self.object.credite.email)
        else:
            emails = [user.email for user in self.object.debiteurs.all() if user.email]
            if (
                self.object.creancier.email
                and self.object.creancier.email not in emails
            ):
                emails.append(self.object.creancier.email)
            subject += "e"
        send_mail(
            subject,
            f"comptes/mail_{model.lower()}.md",
            settings.DEFAULT_FROM_EMAIL,
            emails,
            ctx,
            self.request,
        )

    def get_context_data(self, **kwargs):
        """Provide the Occasion to the context for the template."""
        ctx = super(DetteOrRemboursementCreateView, self).get_context_data(**kwargs)
        ctx["occasion"] = self.occasion
        return ctx

    def get_success_url(self):
        """Redirect the user where he wants to go."""
        if "add_another" in self.request.POST:
            return self.request.path
        return super(DetteOrRemboursementCreateView, self).get_success_url()


class DetteCreateView(DetteOrRemboursementCreateView):
    """Specialize DetteOrRemboursementCreateView for Dette."""

    model = Dette
    form_class = DetteForm


class RemboursementCreateView(DetteOrRemboursementCreateView):
    """Specialize DetteOrRemboursementCreateView for Remboursement."""

    model = Remboursement
    form_class = RemboursementForm
