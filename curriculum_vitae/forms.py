'''
Created on Sep. 10, 2020

@author: Louis-Philippe
'''

from .models import Education
from django import forms

class CvEducationCreateForm(forms.ModelForm):
    class Meta:
        model = Education
        exclude = ('psychologue',)