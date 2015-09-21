from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, render

from .models import Occasion


@login_required
def home(request, slug=None):
    if slug is None:
        occasions = Occasion.objects.filter(clos=False).filter(Q(membres__isnull=True) | Q(membres=request.user))
    else:
        occasions = [get_object_or_404(Occasion, slug=slug)]
        if request.user not in occasions[0].get_membres():
            raise Http404
    return render(request, 'comptes/comptes.html', {'occasions': occasions})
