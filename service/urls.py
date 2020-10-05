'''
Created on Sep. 3, 2020

@author: Louis-Philippe
'''
from django.urls import path
from service.views import ServiceUpdateView, ServiceListView, ServiceDetailView, ServiceCreateView, ServiceDeleteView


urlpatterns = [
    path('services/add', ServiceCreateView.as_view(), name='service-add'),
    path('services/<int:pk>/', ServiceUpdateView.as_view(), name='service-update'),
    path('services/delete/<int:pk>', ServiceDeleteView.as_view(), name='service-delete'),
    path('services/list', ServiceListView.as_view(), name='service-list'),
    path('services/details/<int:pk>', ServiceDetailView.as_view(), name='service-detail'),
    ]