# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from comptes.models import Occasion
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, render


@login_required
def home(request, slug=None):
    if slug is None:
        occasions = request.user.occasion_set.filter(clos=False)
    else:
        occasions = [get_object_or_404(Occasion, slug=slug)]
        if request.user not in occasions[0].membres.all():
            raise Http404
    return render(request, 'comptes/comptes.html', {'occasions': occasions})
