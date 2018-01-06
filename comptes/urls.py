from django.urls import path

from .views import DetteCreateView, RemboursementCreateView, home

app_name = 'comptes'
urlpatterns = [
    path('', home, name='home'),
    path('<str:slug>', home, name='occasion'),
    path('<str:oc_slug>/dette', DetteCreateView.as_view(), name='dette'),
    path('<str:oc_slug>/remboursement', RemboursementCreateView.as_view(), name='remboursement'),
]
