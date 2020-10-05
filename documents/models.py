from django.db import models
from users.models import Client, Psychologue
import os
from pathlib import Path


# Create your models here.
def get_upload_path(instance, filename):
    folder_name = (instance.client.last_name+"_"+instance.client.first_name)
    path = Path(os.path.join('clients', folder_name, 'test_'+instance.extension()))
    Path(path).mkdir(parents=True, exist_ok=True)
    
    return path


class DocumentType(models.Model):
    nom = models.CharField(max_length=40)
    psychologue = models.ForeignKey(Psychologue, on_delete=models.CASCADE)
    def __str__(self):
        return self.nom


class Document(models.Model):
    nom = models.CharField(max_length=100)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    file_extention = models.CharField(max_length=5, blank=True, null=True)
    type=models.ForeignKey(DocumentType, on_delete=models.CASCADE)
    description = models.CharField(max_length=50)
    docfile = models.FileField(upload_to=get_upload_path)
    
    def extension(self):
        name, extension = os.path.splitext(self.docfile.name)
        return extension
    