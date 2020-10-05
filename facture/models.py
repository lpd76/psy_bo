from django.db import models
from service.models import Service
from users.models import Client, Psychologue  
from django.utils import timezone
from django.db.models import Sum, F, FloatField

#from paiement.models import Paiement



# Create your models here.

class Facture(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    psychologue = models.ForeignKey(Psychologue, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now, blank=True)
    is_active = models.BooleanField(default=True)
    close_date = models.DateField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    paid_date = models.DateField(blank=True, null=True)
    def __str__(self):
        return str(self.date) + " " +self.client.first_name +" " +self.client.last_name
    class Meta:
        ordering = ['-date']

class PrestationManager(models.Manager):
    
    def get_bill_details(self, facture_id): 
        service_list = self.filter(facture=facture_id)
        sous_total = service_list.aggregate(sous_total= Sum(F('qte') * F('prix'), output_field=FloatField()))
        if len(service_list)>=1:
            sous_total = sous_total['sous_total']
        else:
            sous_total=0
        montant_tvq = round(sous_total*0.09975,2)
        montant_tps = round(sous_total*0.05,2)
        total = sous_total+montant_tvq+montant_tps
        return {'service_list':service_list, 'sous_total':sous_total, 'tvq':montant_tvq, 'tps':montant_tps, 'total':total}
    
#     def get_pmt_total_amount(self, facture_id):
#         facture = Facture.objects.aggregate(total=sum('paiement__montant'))
#         #facture = facture.aggregate(total=sum('paiement__montant'))
#         pmt = facture['total']
#         return pmt         
class PrestationDeService(models.Model):
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE)
    #date du calendrier
    date = models.DateTimeField(default=timezone.now, blank=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    qte = models.DecimalField(max_digits=6, decimal_places=2)
    prix = models.DecimalField(max_digits=6, decimal_places=2)
    objects = models.Manager()
    sous_total = PrestationManager()
    def montant(self):
        self.montant = self.qte * self.prix
        return round(self.montant, 2)  
    class Meta:
        ordering = ['-date']

    

        
    