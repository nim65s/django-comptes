from django.conf.urls import patterns, url

from .views import DetteCreateView, RemboursementCreateView, home

urlpatterns = patterns('',
    url(r'^$', home, name='home'),
    url(r'^(?P<slug>[^/]+)$', home, name='occasion'),
    url(r'^(?P<oc_slug>[^/]+)/dette$', DetteCreateView.as_view(), name='dette'),
    url(r'^(?P<oc_slug>[^/]+)/remboursement$', RemboursementCreateView.as_view(), name='remboursement'),
)
