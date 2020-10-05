from django.db import models
from users.models import Client, Psychologue
from service.models import Service
from django.urls import reverse
from django.utils import timezone


# Create your models here.
class NoteType(models.Model):
    psychologue = models.ForeignKey(Psychologue, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nom

class Note(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    start_date = models.DateTimeField(default=timezone.now, blank=True)
    end_date = models.DateTimeField(default=timezone.now, blank=True)
    type = models.ForeignKey(NoteType, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    note = models.TextField(blank=True)
    def get_absolute_url(self):
        client = self.client
        return reverse('clientdetails2', args=[str(client.id)])
#     def __str__(self):
#         #return self.client.user.first_name+" "+self.type+" "+str(self.date)
#         return self.type
