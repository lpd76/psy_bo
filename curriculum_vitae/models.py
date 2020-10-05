from django.db import models
from users.models import Psychologue
from django.urls import reverse
# from datetime import date, timedelta
# Create your models here.

class ElementCV(models.Model):
    psychologue = models.ForeignKey(Psychologue, on_delete=models.CASCADE)
    nom = models.CharField(max_length=500)
    

class Education(ElementCV):
    CERTIFICATION = 'CR'
    FORMATIONCONTINUE = 'FC'
    EDUCATION_TYPE = [
        (CERTIFICATION, 'Certification'),
        (FORMATIONCONTINUE, 'Formation Continue'),
    ]
    institution = models.CharField(max_length=200, blank=True, null=True)
    institute_url = models.URLField(blank=True, null=True)
    formateur = models.CharField(max_length=200, blank=True, null=True)
    formateur_url = models.URLField(blank=True, null=True)
    date_obtention = models.DateField()
    type = models.CharField(
        max_length=2,
        choices=EDUCATION_TYPE,
        default=FORMATIONCONTINUE,
    )
    def __str__(self):
        return self.nom
    def get_absolute_url(self):
        return reverse('education-detail', kwargs={'pk': self.pk})

class ExpérienceProfessionelle(ElementCV):
    EXPERIENCETRAVAIL = 'ET'
    ACTIVITEACADEMIQUE = 'AA'
    CORPORATIONPROFESSIONELLE = 'CP'
    EXPERIENCE_TYPE = [
        (EXPERIENCETRAVAIL, 'expériences de travail'),
        (ACTIVITEACADEMIQUE, 'activité academique'),
        (CORPORATIONPROFESSIONELLE, 'corporations ou sociétés professionnelle'),
    ]
    
    date_debut = models.DateField()
    date_fin = models.DateField(blank=True, null=True)
    description = models.CharField(max_length=200)
    type = models.CharField(
        max_length=2,
        choices=EXPERIENCE_TYPE,
        default=EXPERIENCETRAVAIL,
    )
    
    def __str__(self):
        return self.nom
    
    def get_absolute_url(self):
        return reverse('exppro-detail', kwargs={'pk': self.pk})
    
            
    
class CorporationProfessionelle(ElementCV):
    date_debut = models.DateField()
    date_fin = models.DateField(blank=True, null=True)
    description = models.CharField(max_length=200)
    
    def __str__(self):
        return self.nom
    
    def is_active_member(self):
        self.member_status = False
        if self.date_fin:
            pass
        else:
            self.member_status = True
        return self.member_status
             
        
    
    def get_absolute_url(self):
        return reverse('corpopro-detail', kwargs={'pk': self.pk})

class AssociationProfessionelle(ElementCV):
    permis = models.CharField(max_length=20,blank=True, null=True)
    date_debut = models.DateField(blank=True, null=True)
    date_fin = models.DateField(blank=True, null=True)
    
    
    def __str__(self):
        return self.nom
    
    def is_active_member(self):
        self.member_status = False
        if self.date_fin:
            pass
        else:
            self.member_status = True
        return self.member_status
    
    def get_absolute_url(self):
        return reverse('associationpro-detail', kwargs={'pk': self.pk})
    
class Conference(ElementCV):
    date = models.DateField()
    organisme = models.CharField(max_length=200)
    titre = models.CharField(max_length=200)
    lieu = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    
    def __str__(self):
        return self.nom
    
    def get_absolute_url(self):
        return reverse('conference-detail', kwargs={'pk': self.pk})
    
    

    