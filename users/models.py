from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from phone_field import PhoneField

# Create your models here.
class CustomUser(AbstractUser):
    door_number = models.SmallIntegerField(blank=True, null=True)
    app_number = models.CharField(max_length=10, blank=True, null=True)
    street_name = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=7, blank=True)
    province = models.CharField(max_length=5, default = 'Qc')
    country = models.CharField(max_length=50, default='Canada')
    cell_phone = PhoneField(blank=True, help_text='Contact phone number')

    def __str__(self):
        return self.username
  
class Psychologue(CustomUser):
    is_client = models.BooleanField(default = False)
    is_psychologist = models.BooleanField(default = True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, parent_link=True)
    permis_num = models.CharField(max_length=15, blank=True, null=True)
    permis_date = models.DateField(blank=True, default='2018-01-01', null=True)
    avatar = models.ImageField(upload_to = 'media/profile_picture/')
    phone = PhoneField(blank=True, help_text='Contact phone number')
    fax = models.CharField(max_length=10, blank=True)
    bio = models.TextField(max_length=1700, blank=True)
    education = models.CharField(max_length=70, blank=True)
    site_web = models.URLField(blank=True)
    linked_in = models.URLField(blank=True)
    tps = models.CharField(max_length=20, blank=True, null=True)
    tvq = models.CharField(max_length=20, blank=True, null=True)
    USERNAME_FIELD = 'email'
    def __str__(self):
        user_info = Psychologue.objects.get(id=self.user_id)
        return user_info.first_name + ' ' + user_info.last_name
    class Meta:
        verbose_name = 'Psychologue'
        verbose_name_plural = 'Psychologues'
    def get_absolute_url(self):
            return reverse('profile', kwargs={'pk': self.pk})
   
class Client(CustomUser):
    psychologue_traitant = models.ForeignKey(Psychologue, on_delete=models.CASCADE)
    is_client = models.BooleanField(default = True)
    is_psychologist = models.BooleanField(default = False)
    is_male = models.BooleanField(default=False)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, parent_link=True)
    dob = models.DateField(null=True)
    USERNAME_FIELD = 'email'
    def __str__(self):
        user_info = Client.objects.get(id=self.user_id)
        return user_info.first_name + ' ' + user_info.last_name
    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
    def get_absolute_url(self):
            return reverse('clientdetails2', kwargs={'pk': self.pk})
    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in Client._meta.fields]
        
class Conferencier(CustomUser):
    education = models.CharField(max_length=70, blank=True)
    site_web = models.URLField(blank=True)
    linked_in = models.URLField(blank=True)
    class Meta:
        verbose_name = 'Conférencier'
        verbose_name_plural = 'Conférenciers'