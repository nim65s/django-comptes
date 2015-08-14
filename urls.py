from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from .views import home

urlpatterns = patterns('',
    url(r'^$', home, name='home'),
    url(r'^faq$', TemplateView.as_view(template_name='comptes/faq.html'), name="faq"),
    url(r'^about$', TemplateView.as_view(template_name='comptes/about.html'), name="about"),
    url(r'^(?P<slug>[^/]+)$', home, name='occasion'),
)
