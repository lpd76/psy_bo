'''
Created on Sep. 4, 2020

@author: Louis-Philippe
'''
from django.urls import path
from curriculum_vitae.views import EducationCreate, EducationUpdate, EducationDelete,\
    ExpérienceProfessionelleCreate, ExpérienceProfessionelleUpdate,\
    ExpérienceProfessionelleDelete, CorporationProfessionelleCreate,\
    CorporationProfessionelleUpdate, CorporationProfessionelleDelete,\
    AssociationProfessionelleCreate, AssociationProfessionelleUpdate,\
    AssociationProfessionelleDelete, ConferenceCreate, ConferenceUpdate,\
    ConferenceDelete, EducationListView, ExpérienceProfessionelleListView,\
    AssociationProfessionelleListView, ConferenceListView,\
    EducationDetailView, ExpérienceProfessionelleDetailView,\
    CorporationProfessionelleListView, CvEducationView
    #CvEducationView
#from . import views
    
    
urlpatterns = [
    # ...
    path('education/add/', EducationCreate.as_view(), name='education-add'),
    path('education/<int:pk>/', EducationUpdate.as_view(), name='education-update'),
    path('education/delete/<int:pk>', EducationDelete.as_view(), name='education-delete'),
    path('education/list', EducationListView.as_view(), name='education-list'),
    path('education/details/<int:pk>', EducationDetailView.as_view(), name='education-detail'),
    
    path('experiences/add/', ExpérienceProfessionelleCreate.as_view(), name='experience-add'),
    path('experiences/<int:pk>/', ExpérienceProfessionelleUpdate.as_view(), name='experience-update'),
    path('experiences/delete/<int:pk>', ExpérienceProfessionelleDelete.as_view(), name='experience-delete'),
    path('experiences/list', ExpérienceProfessionelleListView.as_view(), name='experience-list'),
    path('experiences/details/<int:pk>', ExpérienceProfessionelleDetailView.as_view(), name='experience-detail'),
    
    path('corporations/add/', CorporationProfessionelleCreate.as_view(), name='corporation-add'),
    path('corporations/<int:pk>/', CorporationProfessionelleUpdate.as_view(), name='corporation-update'),
    path('corporations/<int:pk>/delete/', CorporationProfessionelleDelete.as_view(), name='corporation-delete'),
    path('corporation/list', CorporationProfessionelleListView.as_view(), name='corporation-list'),
    
    path('associations/add/', AssociationProfessionelleCreate.as_view(), name='association-add'),
    path('associations/<int:pk>/', AssociationProfessionelleUpdate.as_view(), name='association-update'),
    path('associations/<int:pk>/delete/', AssociationProfessionelleDelete.as_view(), name='association-delete'),
    path('association/list', AssociationProfessionelleListView.as_view(), name='association-list'),
    
    path('conference/add/', ConferenceCreate.as_view(), name='conference-add'),
    path('conference/<int:pk>/', ConferenceUpdate.as_view(), name='conference-update'),
    path('conference/delete/<int:pk>', ConferenceDelete.as_view(), name='conference-delete'),
    path('conference/list', ConferenceListView.as_view(), name='conference-list'),
    
#    path('<int:pk>', CvEducationView.as_view(), name='cv'),
    path('test/<int:pk>', CvEducationView, name='cv'),
]