
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView, DetailView
from .models import Service
from users.models import Psychologue

# Create your views here.

class ServiceCreateView(LoginRequiredMixin, CreateView):
    model = Service
    fields = ('nom', 'description', 'unit', 'suggested_price')
    
    def form_valid(self, form):
        psychologue = Psychologue.objects.get(id = self.request.user.id)
        form.instance.psychologue = psychologue
        return super(ServiceCreateView, self).form_valid(form)
    
    def get_success_url(self):
        """Detect the submit button used and act accordingly"""
        if 'service-add' in self.request.POST:
            url = reverse_lazy('service-add')
        else:
            url = reverse_lazy('service-list')
        return url

class ServiceUpdateView(LoginRequiredMixin, UpdateView):
    model = Service
    fields = ('nom', 'description', 'unit', 'suggested_price')
    success_url = reverse_lazy('service-list')
    
class ServiceDeleteView(LoginRequiredMixin, DeleteView):
    model = Service
    success_url = reverse_lazy('service-list')
    
class ServiceListView(ListView):
    model = Service
    def get_queryset(self):
        psy_id = Psychologue.objects.get(id=self.request.user.id)
        return Service.objects.filter(psychologue__id = psy_id.id)
        
class ServiceDetailView(DetailView):
    model = Service
    context_object_name = 'service_detail'
    