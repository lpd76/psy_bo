'''
Created on Sep. 17, 2020

@author: Louis-Philippe
'''
from django.urls import path 
from paiement.views import PaiementCreateView, PaiementUpdateView,\
    PaiementDeleteView, PaiementListView, PaiementDetailView



urlpatterns = [
    path('paiement/create/<int:pk>', PaiementCreateView.as_view(), name='paiement-add'),
    path('paiement/update/<int:pk>', PaiementUpdateView.as_view(), name='paiement-update'),
    path('paiement/delete/<int:pk>', PaiementDeleteView.as_view(), name='paiement-delete'),
    path('paiement/list/<int:pk>', PaiementListView.as_view(), name='paiement-list'),
    path('paiement/details/<int:pk>', PaiementDetailView.as_view(), name='paiement-detail'),
   
    ]