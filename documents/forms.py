'''
Created on Sep. 14, 2020

@author: Louis-Philippe
'''
from django import forms
from .models import Document


class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('description', 'type', 'docfile', )
#     def form_valid(self, form):
#         client = Client.objects.get(id = self.kwargs['pk'])
#         form.instance.client = client
#         return super(DocumentForm, self).form_valid(form)
