#-*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404

from comptes.models import Dette, Remboursement, Occasion


@login_required
def home(request, slug=None):
    if slug is None:
        occasions = request.user.occasion_set.filter(clos=False)
    else:
        occasions = [get_object_or_404(Occasion, slug=slug)]
        if request.user not in occasions[0].membres.all():
            raise Http404
    return render(request, 'comptes/comptes.html', {'occasions': occasions})
