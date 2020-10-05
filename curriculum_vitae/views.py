
# Create your views here.
# from django.shortcuts import get_object_or_404
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView, DetailView
from .models import Education, ExpérienceProfessionelle, CorporationProfessionelle, AssociationProfessionelle, Conference
from users.models import Psychologue

################Education############################################

class EducationCreate(LoginRequiredMixin, CreateView):
    model = Education
    fields = ('nom', 'institution', 'institute_url', 
              'formateur', 'formateur_url', 'date_obtention', 'type')
    
    def form_valid(self, form):
        psychologue = Psychologue.objects.get(id = self.request.user.id)
        form.instance.psychologue = psychologue
        return super(EducationCreate, self).form_valid(form)
    
    def get_success_url(self):
        """Detect the submit button used and act accordingly"""
        if 'education-add' in self.request.POST:
            url = reverse_lazy('education-add')
        else:
            url = reverse_lazy('education-list')
        return url

class EducationUpdate(UpdateView):
    model = Education
    fields = ('nom', 'institution', 'institute_url', 
              'formateur', 'formateur_url', 'date_obtention', 'type')

class EducationDelete(DeleteView):
    model = Education
    success_url = reverse_lazy('education-list')
    
class EducationListView(ListView):
    model = Education
    def get_queryset(self):
        psy_id = Psychologue.objects.get(id=self.request.user.id)
        return Education.objects.filter(psychologue__id = psy_id.id)
    context_object_name = 'education_list'
    
class EducationDetailView(DetailView):
    model = Education
    
def CvEducationView(request, pk):
    psy_info = get_object_or_404(Psychologue, id=pk)
    cv_education = Education.objects.filter(psychologue=pk) 
    cv_experience = ExpérienceProfessionelle.objects.filter(psychologue=psy_info.id)
    cv_conference = Conference.objects.filter(psychologue=psy_info.id)
    cv_association = AssociationProfessionelle.objects.filter(psychologue=psy_info.id)
    return render(request, 'psy/cv.html', {'psy_profile':psy_info, 
                                       'education_list':cv_education, 
                                       'cv_experience':cv_experience,
                                       'conference_list':cv_conference,
                                       'association_list':cv_association})
    
    
    
################Experience############################################ 

class ExpérienceProfessionelleCreate(CreateView):
    model = ExpérienceProfessionelle
    fields = ('nom', 'date_debut', 'date_fin', 'description', 'type')
    
    def form_valid(self, form):
        psychologue = Psychologue.objects.get(id = self.request.user.id)
        form.instance.psychologue = psychologue
        return super(ExpérienceProfessionelleCreate, self).form_valid(form)
    
    def get_success_url(self):
        """Detect the submit button used and act accordingly"""
        if 'experience-add' in self.request.POST:
            url = reverse_lazy('experience-add')
        else:
            url = reverse_lazy('experience-list')
        return url

class ExpérienceProfessionelleUpdate(UpdateView):
    model = ExpérienceProfessionelle
    fields = ('nom', 'date_debut', 'date_fin', 'description', 'type')
    success_url = reverse_lazy('experience-list')

class ExpérienceProfessionelleDelete(DeleteView):
    model = ExpérienceProfessionelle
    success_url = reverse_lazy('experience-list')
    
class ExpérienceProfessionelleListView(ListView):
    model = ExpérienceProfessionelle
    def get_queryset(self):
        psy = Psychologue.objects.get(id=self.request.user.id)
        return ExpérienceProfessionelle.objects.filter(psychologue__id = psy.id)
    context_object_name = 'experience_list'
    
class ExpérienceProfessionelleDetailView(DetailView):
    model = ExpérienceProfessionelle



################Corporation############################################  

class CorporationProfessionelleCreate(CreateView):
    model = CorporationProfessionelle
    fields = "__all__"

class CorporationProfessionelleUpdate(UpdateView):
    model = CorporationProfessionelle
    fields = "__all__"

class CorporationProfessionelleDelete(DeleteView):
    model = CorporationProfessionelle
    success_url = reverse_lazy('corporation-list')
    
class CorporationProfessionelleListView(ListView):
    model = CorporationProfessionelle
    
class CorporationProfessionelleDetailView(DetailView):
    model = CorporationProfessionelle
    
    
################association############################################   

class AssociationProfessionelleCreate(CreateView):
    model = AssociationProfessionelle
    fields = ('nom', 'permis', 'date_debut', 'date_fin')
    
    def form_valid(self, form):
        psychologue = Psychologue.objects.get(id = self.request.user.id)
        form.instance.psychologue = psychologue
        return super(AssociationProfessionelleCreate, self).form_valid(form)
    
    def get_success_url(self):
        """Detect the submit button used and act accordingly"""
        if 'association-add' in self.request.POST:
            url = reverse_lazy('association-add')
        else:
            url = reverse_lazy('association-list')
        return url

class AssociationProfessionelleUpdate(UpdateView):
    model = AssociationProfessionelle
    fields = ('nom', 'permis', 'date_debut', 'date_fin')
    success_url = reverse_lazy('association-list')

class AssociationProfessionelleDelete(DeleteView):
    model = AssociationProfessionelle
    success_url = reverse_lazy('association-list')
    
class AssociationProfessionelleListView(ListView):
    model = AssociationProfessionelle
    context_object_name = 'association_list'
    
    def get_queryset(self):
        psy = Psychologue.objects.get(id=self.request.user.id)
        return AssociationProfessionelle.objects.filter(psychologue__id = psy.id)
    
class AssociationProfessionelleDetailView(DetailView):
    model = AssociationProfessionelle

    
################Conference############################################

class ConferenceCreate(CreateView):
    model = Conference
    fields = ('nom', 'date', 'organisme', 'titre', 'lieu', 'description' )
    
    def form_valid(self, form):
        psychologue = Psychologue.objects.get(id = self.request.user.id)
        form.instance.psychologue = psychologue
        return super(ConferenceCreate, self).form_valid(form)
    
    def get_success_url(self):
        """Detect the submit button used and act accordingly"""
        if 'conference-add' in self.request.POST:
            url = reverse_lazy('conference-add')
        else:
            url = reverse_lazy('conference-list')
        return url

class ConferenceUpdate(UpdateView):
    model = Conference
    fields = ('nom', 'date', 'organisme', 'titre', 'lieu', 'description' )

class ConferenceDelete(DeleteView):
    model = Conference
    success_url = reverse_lazy('conference-list')
    
class ConferenceListView(ListView):
#     model = Conference
#     context_object_name = 'conference_list'
#     template_name = 'conference_list22.html'
    
    def get_queryset(self):
        psy = Psychologue.objects.get(id=self.request.user.id)
        return Conference.objects.filter(psychologue__id = psy.id)
    
class ConferenceDetailView(DetailView):
    model = Conference
    
    