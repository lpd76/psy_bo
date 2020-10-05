
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView, DetailView
from .models import Paiement
from .forms import PaiementCreateForm
from decimal import Decimal


from facture.models import Facture, PrestationDeService
from bootstrap_datepicker_plus import DatePickerInput  # @UnresolvedImport

# Create your views here.
class PaiementCreateView(LoginRequiredMixin, CreateView):
    form_class = PaiementCreateForm
    template_name = 'paiement/paiement_form.html'
    
    def get_form(self, obj=None, **kwargs):
        facture_id = self.kwargs['pk']
        montant_details = Paiement.montant_verse.get_pmt_details(facture_id)
        service_details = PrestationDeService.sous_total.get_bill_details(facture_id)
        montant_total_facture = service_details['total']
        if montant_details['total_pmt']:
            montant_total_pmt = montant_details['total_pmt']
        else:
            montant_total_pmt=0
        solde = Decimal(montant_total_facture) - montant_total_pmt
        form = super(PaiementCreateView, self).get_form()
        form.fields['date'].widget = DatePickerInput()
        form.fields['montant'].initial = round(solde, 2)
        #form.fields['montant'].value = 100
        return form
    
#     def get_context_data(self, **kwargs):
#         """ get_context_data let you fill the template context """
#         context = super(PaiementCreateView, self).get_context_data(**kwargs)
#         facture=Facture.objects.get(id=self.kwargs['pk'])
#         prestation_list = PrestationDeService.objects.filter(facture=facture.id)
#         detail_montant = PrestationDeService.sous_total.get_total_amount(self.kwargs['pk'])
#         detail_pmts = Paiement.objects.filter(facture=facture)
#         pmts_total = Paiement.montant_verse.get_total_amount(self.kwargs['pk'])
#         
#         context['facture'] = facture
#         context['prestation_list'] = prestation_list
#         context['prestation_total'] = detail_montant
#         context['pmt_list'] = detail_pmts
#         context['pmt_total'] = pmts_total
#         return context
    
    def form_valid(self, form):
        facture = Facture.objects.get(id=self.kwargs['pk'])
        form.instance.facture = facture
        form.instance.client = facture.client
        return super(PaiementCreateView, self).form_valid(form)
#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs['pk'] = self.kwargs['pk']
#         return kwargs
    def get_success_url(self):
        """Detect the submit button used and act accordingly"""
        #client_id = self.kwargs['pk']
        if 'paiement-add' in self.request.POST:
            url = reverse_lazy('paiement-add', kwargs={'pk': self.kwargs['pk']})
        else:
            url = reverse_lazy('clientdetails2', kwargs={'pk': Facture.objects.get(id=self.kwargs['pk']).client.id})
        return url
    
class PaiementUpdateView(LoginRequiredMixin, UpdateView):
    model = Paiement
    fields = ('date','facture', 'montant', )
    def get_form(self):
        form = super().get_form()
        form.fields['date'].widget = DatePickerInput()
        return form

class PaiementDeleteView(LoginRequiredMixin, DeleteView):
    model = Paiement
    success_url = reverse_lazy('paiement-list')
    
class PaiementListView(LoginRequiredMixin, ListView):
    model = Paiement
    
    
class PaiementDetailView(LoginRequiredMixin, DetailView):
    model = Paiement
    context_object_name = 'paiement'