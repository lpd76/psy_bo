'''
Created on Sep. 3, 2020

@author: Louis-Philippe
'''
from django.urls import path
from facture.views import FactureCreateView, FactureUpdateView,\
    FactureDeleteView, FactureListView, FactureDetailView,\
    PrestationDeServiceCreateView, PrestationDeServiceUpdateView,\
    PrestationDeServiceDeleteView, PrestationDeServiceListView,\
    PrestationDeServiceDetailView, get_service_attributes, pdf_view, write_facture_pdf_view2, write_recut_pdf_view,\
    fermer_facture_view, envoyer_facture_view
    

urlpatterns = [
    path('add/<int:pk>', FactureCreateView.as_view(), name='facture-add'),
    path('update/<int:pk>/', FactureUpdateView.as_view(), name='facture-update'),
    path('delete/<int:pk>', FactureDeleteView.as_view(), name='facture-delete'),
    path('list', FactureListView.as_view(), name='facture-list'),
    path('details/<int:pk>', FactureDetailView.as_view(), name='facture-detail'),
    
    path('prestationdeservice/add/<int:pk>', PrestationDeServiceCreateView.as_view(), name='prestationdeservice-add'),
    path('prestationdeservice/update/<int:pk>', PrestationDeServiceUpdateView.as_view(), name='prestationdeservice-update'),
    path('prestationdeservice/delete/<int:pk>', PrestationDeServiceDeleteView.as_view(), name='prestationdeservice-delete'),
    path('prestationdeservice/list', PrestationDeServiceListView.as_view(), name='prestationdeservice-list'),
    path('prestationdeservice/details/<int:pk>', PrestationDeServiceDetailView.as_view(), name='prestationdeservice-detail'),
    
    path('ajax', get_service_attributes, name='ajax-sevice'),
    path('pdf', pdf_view, name='pdf_view'),
    path('pdf/<int:pk>', write_facture_pdf_view2, name='pdf_view2'),
    path('recut/pdf/<int:pk>', write_recut_pdf_view, name='recut_pdf_view'),
    path('fermer/<int:pk>', fermer_facture_view, name='facture-fermer'),
    path('send_mail/<int:pk>', envoyer_facture_view, name='facture-envoyer'),
    ]