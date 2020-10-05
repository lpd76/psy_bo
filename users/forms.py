'''
Created on Aug. 28, 2020

@author: Louis-Philippe
'''
# from django import forms

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Psychologue, Client

class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = CustomUser
#       fields = "__all__" 
        fields = ('username', 'email', 'door_number', 
                  'app_number', 'street_name', 'city', 
                  'postal_code', 'province', 'country',)
        
class CustomUserChangeForm(UserChangeForm):
    
    class Meta:
        model = CustomUser
#         fields = ('username', 'email', 'is_client', 
#                   'is_psychologist', 'door_number', 
#                   'app_number', 'street_name', 'city', 
#                   'postal_code', 'province', 'country',)
        fields = "__all__" 
        
class PsychologueCreationForm(UserCreationForm):
    
    class Meta:
        model = Psychologue
#        fields = "__all__" 
        fields = ('first_name', 'last_name', 'username', 'email', 'door_number', 
                  'app_number', 'street_name', 'city', 
                  'postal_code', 'province', 'country',
                  'permis_num', 'permis_date', 'tps','tvq', 'avatar', 
                 'phone', 'fax','bio', 'education', 
                 'site_web','linked_in',)
            
        
class PsychologueChangeForm(UserChangeForm):
    
    class Meta:
        model = Psychologue
#        fields = "__all__" 
        fields = ('email', 'door_number', 
                  'app_number', 'street_name', 'city', 
                  'postal_code','avatar', 
                 'phone', 'fax','bio','permis_num', 'tps','tvq', 
                 'site_web','linked_in',)
        
        
class ClientCreationForm(UserCreationForm):
    
    class Meta:
        model = Client
        #fields = "__all__" 
        fields = ('first_name', 'last_name', 'is_male', 'username', 'email', 'cell_phone', 'door_number', 
                  'app_number', 'street_name', 'city', 
                  'postal_code', 'province', 'country', 'dob',)
        
class ClientChangeForm(UserChangeForm):
    
    class Meta:
        model = Client
        #fields = "__all__" 
        fields = ('first_name', 'last_name', 'username', 'email', 'cell_phone','door_number', 
                  'app_number', 'street_name', 'city', 
                  'postal_code', 'province', 'country', 'dob',)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        