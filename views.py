#-*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from comptes.models import Dette, Remboursement, Occasion

@login_required
def home(request, slug=None):
    if slug is None:
        occasions = request.user.occasion_set.filter(clos=False)
    else:
        occasions = [get_object_or_404(Occasion, slug=slug)]
    return render(request, 'comptes/occasions.html', {'occasions': occasions})
