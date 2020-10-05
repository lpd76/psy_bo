'''
Created on Sep. 3, 2020

@author: Louis-Philippe
'''
from .models import Facture
from django.forms import ModelForm

class FactureCreateForm(ModelForm):
    class Meta:
        model= Facture
        fields ="__all__"

