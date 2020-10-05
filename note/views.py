
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView, DetailView
from .models import Note, NoteType
from users.models import Psychologue, Client
from bootstrap_datepicker_plus import DatePickerInput  # @UnresolvedImport

# Create your views here.

class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    fields = ('start_date','end_date','service', 'note')
    # ajouter le calendrier
    def get_form(self):
        form = super().get_form()
        form.fields['start_date'].widget = DatePickerInput(format='%Y-%m-%d %H:%M')
        form.fields['end_date'].widget = DatePickerInput(format='%Y-%m-%d %H:%M')
        return form
    # ajoute le client automatiquement
    def form_valid(self, form):
        client = Client.objects.get(id = self.kwargs['pk'])
        form.instance.client = client
        return super(NoteCreateView, self).form_valid(form)
    def get_success_url(self):
        """Detect the submit button used and act accordingly"""
        #client_id = self.kwargs['pk']
        if 'note-add' in self.request.POST:
            url = reverse_lazy('note-add', kwargs={'pk': self.kwargs['pk']})
        else:
            url = reverse_lazy('clientdetails2', kwargs={'pk': self.kwargs['pk']})
        return url

class NoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Note
    fields = ('start_date', 'end_date', 'service', 'note')
    def get_form(self):
        form = super().get_form()
        form.fields['start_date'].widget = DatePickerInput(format='%Y-%m-%d %H:%M')
        form.fields['end_date'].widget = DatePickerInput(format='%Y-%m-%d %H:%M')
        return form

class NoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Note
    def get_client(self):
        note = super(NoteDeleteView, self).get_object()
        client = note.client
        return client
    def get_success_url(self):
        url = reverse_lazy('clientdetails2', kwargs={'pk': self.get_client().id})
        return url
    
class NoteListView(LoginRequiredMixin, ListView):
    model = Note
    def get_queryset(self):
        client = Client.objects.get(id = self.kwargs['pk'])
        return Note.objects.filter(client = client.id)
    context_object_name = 'note_list'
    
class NoteDetailView(LoginRequiredMixin, DetailView):
    model = Note
    
######################### Note Type ################################################################   

class NoteTypeCreateView(LoginRequiredMixin, CreateView):
    model = NoteType
    fields = ('nom',)
    # ajoute le client automatiquement
    def form_valid(self, form):
        psychologue = Psychologue.objects.get(id = self.request.user.id)
        form.instance.psychologue = psychologue
        return super(NoteTypeCreateView, self).form_valid(form)
    def get_success_url(self):
        """Detect the submit button used and act accordingly"""
        if 'notetype-add' in self.request.POST:
            url = reverse_lazy('notetype-add')
        else:
            url = reverse_lazy('notetype-list')
        return url

class NoteTypeUpdateView(LoginRequiredMixin, UpdateView):
    model = NoteType
    fields = ('nom',)

class NoteTypeDeleteView(LoginRequiredMixin, DeleteView):
    model = NoteType
    success_url = reverse_lazy('notetype-list')
    
class NoteTypeListView(LoginRequiredMixin, ListView):
    model = NoteType
    def get_queryset(self):
        psychologue = Psychologue.objects.get(id = self.kwargs['pk'])
        return NoteType.objects.filter(psychologue = psychologue.id)
    context_object_name = 'notetype_list'
    
class NoteTypeDetailView(LoginRequiredMixin, DetailView):
    model = NoteType
    context_object_name = 'notetype'