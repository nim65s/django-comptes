# -*- coding: utf-8

from __future__ import unicode_literals

from .views import home
from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^$', home, name='home'),
    url(r'^occasion/(?P<slug>[^/]+)$', home, name='occasion'),
    url(r'^faq$', TemplateView.as_view(template_name='comptes/faq.html'), name="faq"),
    url(r'^about$', TemplateView.as_view(template_name='comptes/about.html'), name="about"),
)
