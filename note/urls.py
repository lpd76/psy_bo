'''
Created on Sep. 16, 2020

@author: Louis-Philippe
'''
from django.urls import path 
from note.views import NoteCreateView, NoteUpdateView, NoteDeleteView,\
    NoteListView, NoteDetailView, NoteTypeCreateView, NoteTypeUpdateView,\
    NoteTypeDeleteView, NoteTypeListView, NoteTypeDetailView


urlpatterns = [
    
    path('note/create/<int:pk>', NoteCreateView.as_view(), name='note-add'),
    path('note/update/<int:pk>', NoteUpdateView.as_view(), name='note-update'),
    path('note/delete/<int:pk>', NoteDeleteView.as_view(), name='note-delete'),
    path('note/list/<int:pk>', NoteListView.as_view(), name='note-list'),
    path('note/details/<int:pk>', NoteDetailView.as_view(), name='note-detail'),
    
    path('notetype/create', NoteTypeCreateView.as_view(), name='notetype-add'),
    path('update/<int:pk>', NoteTypeUpdateView.as_view(), name='notetype-update'),
    path('delete/<int:pk>', NoteTypeDeleteView.as_view(), name='notetype-delete'),
    path('list/<int:pk>', NoteTypeListView.as_view(), name='notetype-list'),
    path('details/<int:pk>', NoteTypeDetailView.as_view(), name='notetype-detail'),
    
    ]