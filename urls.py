from django.conf.urls import patterns, url

from .views import DetteCreateView, home

urlpatterns = patterns('',
    url(r'^$', home, name='home'),
    url(r'^(?P<slug>[^/]+)$', home, name='occasion'),
    url(r'^(?P<oc_slug>[^/]+)/dette$', DetteCreateView.as_view(), name='add_dette'),
)
