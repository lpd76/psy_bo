from django.contrib import admin
# from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm, PsychologueChangeForm, PsychologueCreationForm, ClientCreationForm, ClientChangeForm
from .models import CustomUser, Psychologue, Client

# Register your models here.

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', ]
    
class PsychologueAdmin(UserAdmin):
    add_form = PsychologueCreationForm
    form = PsychologueChangeForm
    model = Psychologue
    list_display = ['permis_num', 'permis_date', 'avatar', 
                 'phone', 'fax','bio', 'education', 
                 'site_web','linked_in',]
class ClientAdmin(UserAdmin):
    add_form = ClientCreationForm
    form = ClientChangeForm
    model = Client
    list_display = ['dob',]
    
    
admin.site.register(CustomUser, CustomUserAdmin,)
admin.site.register(Psychologue, PsychologueAdmin,)
admin.site.register(Client, ClientAdmin)
