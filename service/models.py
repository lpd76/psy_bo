from django.db import models
from users.models import Psychologue


# Create your models here.

class Service(models.Model):
    psychologue = models.ForeignKey(Psychologue, on_delete=models.CASCADE)
    nom = models.CharField(max_length=200)
    description = models.CharField(max_length=200, blank=True, null=True)
    unit = models.CharField(max_length=10, blank=True, null=True)
    suggested_price = models.PositiveSmallIntegerField(blank=True, null=True)
    
    def __str__(self):
        return self.nom