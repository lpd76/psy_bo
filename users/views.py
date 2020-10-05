
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DetailView
from django.db.models import Sum, F, FloatField
from .forms import CustomUserCreationForm, PsychologueCreationForm, PsychologueChangeForm, ClientCreationForm, ClientChangeForm
from .models import Psychologue, Client
from facture.models import Facture
from documents.models import Document
from note.models import Note

# Create your views here.

class SignUpView(LoginRequiredMixin, CreateView):
    form_class = CustomUserCreationForm
    template_name = 'Users/signup.html'
    
class PsySignUpView(LoginRequiredMixin, CreateView):
    form_class = PsychologueCreationForm
    template_name = 'psy/psy_signup.html'
    
class PsyUpdateView(LoginRequiredMixin, UpdateView):
    model = Psychologue
    form_class = PsychologueChangeForm
    template_name = 'psy/psy_update.html'
    
class PsyProfileView(DetailView):
    model = Psychologue 
    template_name = 'psy/psy_detail.html'
#    template_name = 'profile_base.html'
    context_object_name = 'psy_profile'
    
class ClientSignUpView(LoginRequiredMixin, CreateView):
    form_class = ClientCreationForm
    template_name = 'client/client_form.html'
    
    def form_valid(self, form):
        psychologue_traitant = Psychologue.objects.get(id = self.request.user.id)
        form.instance.psychologue_traitant = psychologue_traitant
        return super(ClientSignUpView, self).form_valid(form)
        
class ClientDetailsView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'client/client_detail.html'
   
def ClientDetailsView2(request, pk):
    client = get_object_or_404(Client, id=pk)
    facture = Facture.objects.filter(client=client.id).order_by('-date')\
    .annotate(amount = Sum(F("prestationdeservice__prix")*F('prestationdeservice__qte'),output_field=FloatField()))
    document = Document.objects.filter(client=client.id)
    notes = Note.objects.filter(client=client.id).order_by('-start_date')
    return render(request, 
                  'client/client_detail2.html', 
                  {'client':client,
                   'facture_list':facture,
                   'document_list':document,
                   'notes':notes,
                   }
                  )
    
class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientChangeForm
    template_name = 'client/client_form.html'

class PsychologueListClientView(LoginRequiredMixin, ListView):
    model = Client
    context_object_name = 'psy_client_list'
#    template_name = 'psy/psy_client_list.html'
    template_name = 'client/client_list.html'
    
    def get_queryset(self):
        return Client.objects.filter(psychologue_traitant=self.request.user.id)
    
    
    