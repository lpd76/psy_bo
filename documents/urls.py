'''
Created on Sep. 14, 2020

@author: Louis-Philippe
'''
from django.urls import path 
from documents.views import DocumentUpdateView, DocumentDeleteView,\
    DocumentListView, DocumentDetailView, model_form_upload,\
    DocumentTypeCreateView, DocumentTypeUpdateView, DocumentTypeDeleteView,\
    DocumentTypeListView

urlpatterns = [
    
    path('uplaod/<int:pk>', model_form_upload, name='document-uplaod'),
    path('update/<int:pk>', DocumentUpdateView.as_view(), name='document-update'),
    path('delete/<int:pk>', DocumentDeleteView.as_view(), name='document-delete'),
    path('list/<int:pk>', DocumentListView.as_view(), name='document-list'),
    path('details/<int:pk>', DocumentDetailView.as_view(), name='document-detail'),
    
    path('documenttype/add/<int:pk>', DocumentTypeCreateView.as_view(), name='documenttype-add'),
    path('documenttype/<int:pk>/', DocumentTypeUpdateView.as_view(), name='documenttype-update'),
    path('documenttype/<int:pk>/delete/', DocumentTypeDeleteView.as_view(), name='documenttype-delete'),
    path('documenttype/list/<int:pk>', DocumentTypeListView.as_view(), name='documenttype-list'),
    
    
    ]
