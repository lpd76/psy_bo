'''
Created on Sep. 17, 2020

@author: Louis-Philippe
'''
from .models import Paiement
from django.forms import ModelForm

class PaiementCreateForm(ModelForm):
    class Meta:
        model= Paiement
        fields = ('date','type', 'montant', )
        
#         def __init__(self, pk=None, *args, **kwargs):
#             
#             self.field['montant'].initial  = 100
#         
#             super(PaiementCreateForm, self).__init__(*args, **kwargs)
#     def get_context_data(self, **kwargs):
#         pk = kwargs.pop('pk')
#         """ get_context_data let you fill the template context """
#         context = super(PaiementCreateForm, self).get_context_data(**kwargs)
#         # Get Related publishers
#         context['facture'] = self.object.facture.filter(id=pk)
#         return context
#     def __init__(self, *args, **kwargs):
#         pk = kwargs.pop('pk')
#         super().__init__(*args, **kwargs)
        #self.fields['facture'].queryset = Facture.objects.get(id=pk)