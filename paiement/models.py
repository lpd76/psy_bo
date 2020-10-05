from django.db import models
from django.db.models import Sum
#from django.db.models import Sum, F, FloatField
from users.models import Client 
from facture.models import Facture
from django.urls import reverse

# Create your models here.
class PaiementManager(models.Manager):
    def get_pmt_details(self, facture_id):
        pmt_list = self.filter(facture=facture_id)
        total_pmt = pmt_list.aggregate(total=Sum('montant'))
        total_pmt = total_pmt['total']
        return {'pmt_list':pmt_list, 'total_pmt':total_pmt}
    
class Paiement(models.Model):
    INTERACT = 'I'
    CREDIT = 'R'
    MASTERCARD = 'M'
    VISA = 'V'
    CASH = 'C'
    PAIEMENT_TYPE = [
        (INTERACT, 'Interact'),
        (CREDIT, 'Crédit'),
        (MASTERCARD, 'MasterCard'),
        (VISA, 'Visa'),
        (CASH, 'Argent'),   
    ]
    
    date = models.DateField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=6, decimal_places=2)
    type = models.CharField(
        max_length=1,
        choices=PAIEMENT_TYPE,
        default=CREDIT,
    )
    objects = models.Manager()
    montant_verse = PaiementManager()
    
    def get_absolute_url(self):
        client = self.client
        return reverse('clientdetails2', args=[str(client.id)])
    def __str__(self):
        return self.client.first_name+" "+self.client.last_name+" "+str(self.montant)