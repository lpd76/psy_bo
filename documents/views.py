from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView, DetailView
from .forms import DocumentUploadForm
from users.models import Client, Psychologue
from .models import Document, DocumentType

# Create your views here.
@login_required(login_url='login')
def model_form_upload(request, pk):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = DocumentUploadForm(request.POST, request.FILES)
            if form.is_valid():
                document=form.save(commit=False)
                client = Client.objects.get(id=pk)
                document.client = client
                document.nom = document.type.nom
                document.save()
                return redirect('clientdetails2', pk)
        else:
            form = DocumentUploadForm()
        return render(request, 'model_form_upload.html', {
            'form': form
        })
    else:
        pass

class DocumentUpdateView(LoginRequiredMixin, UpdateView):
    model = Document
    fields = "__all__"
    
class DocumentDeleteView(LoginRequiredMixin, DeleteView):
    model = Document
    def get_success_url(self):
        # if you are passing 'pk' from 'urls' to 'DeleteView' for company
        # capture that 'pk' as companyid and pass it to 'reverse_lazy()' function
        client=Client.objects.get(document__id=self.kwargs['pk'])
        return reverse_lazy('clientdetails2', kwargs={'pk': client.id})
    
class DocumentListView(ListView):
    model = Document
    def get_queryset(self):
        client = Client.objects.get(id=self.request.user.id)
        return Client.objects.filter(psychologue__id = client.id)
    context_object_name = 'client_list'
    
class DocumentDetailView(LoginRequiredMixin, DetailView):
    model = Document
    
    
############################################## Document Type #########################################################

class DocumentTypeCreateView(CreateView):
    model = DocumentType
    fields = ('nom', )
    
    def form_valid(self, form):
        psychologue = Psychologue.objects.get(id = self.request.user.id)
        form.instance.psychologue = psychologue
        return super(DocumentTypeCreateView, self).form_valid(form)
    
    def get_success_url(self):
        #psychologue = Psychologue.objects.get(id=self.request.user.id)
        """Detect the submit button used and act accordingly"""
        if 'documenttype-add' in self.request.POST:
            url = reverse_lazy('documenttype-add', kwargs={'pk': self.request.user.id})
        else:
            url = reverse_lazy('documenttype-list', kwargs={'pk': self.request.user.id})
        return url

class DocumentTypeUpdateView(UpdateView):
    model = DocumentType
    fields = "__all__"
    def get_success_url(self):
        """Detect the submit button used and act accordingly"""
        if 'documenttype-add' in self.request.POST:
            url = reverse_lazy('documenttype-add')
        else:
            url = reverse_lazy('documenttype-list')
        return url

class DocumentTypeDeleteView(DeleteView):
    model = DocumentType
    def get_success_url(self):
        # if you are passing 'pk' from 'urls' to 'DeleteView' for company
        # capture that 'pk' as companyid and pass it to 'reverse_lazy()' function
        psychologue=Psychologue.objects.get(documenttype__id=self.kwargs['pk'])
        return reverse_lazy('documenttype-list', kwargs={'pk': psychologue.id})
       
class DocumentTypeListView(ListView):
    model = DocumentType
    
class DocumentTypeDetailView(DetailView):
    model = DocumentType