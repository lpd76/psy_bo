'''
Created on Aug. 28, 2020
@author: Louis-Philippe
'''
from django.urls import path

from .views import SignUpView, PsySignUpView, ClientSignUpView, ClientDetailsView,\
                    PsyUpdateView, PsychologueListClientView, PsyProfileView, ClientUpdateView, ClientDetailsView2



urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('psychologue/signup', PsySignUpView.as_view(), name='psysignup'),
    path('psychologue/update/<int:pk>', PsyUpdateView.as_view(), name='psyupdate'),
    path('psychologue/profile/<int:pk>', PsyProfileView.as_view(), name='profile'),
    path('psychologue/clients', PsychologueListClientView.as_view(), name='psyclientlist'),
    path('psychologue/client/update/<int:pk>', ClientUpdateView.as_view(), name='client-update'),
    path('psychologue/client/signup/<int:pk>', ClientSignUpView.as_view(), name='psyclientcreate'),
    path('psychologue/client/signup', ClientSignUpView.as_view(), name='clientsignup'),
    path('client/details/<int:pk>', ClientDetailsView.as_view(), name='clientdetails'),
    path('client/details2/<int:pk>', ClientDetailsView2, name='clientdetails2'),
    ]
