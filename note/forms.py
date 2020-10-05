'''
Created on Sep. 22, 2020

@author: Louis-Philippe
'''
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput, DateTimePickerInput, MonthPickerInput, YearPickerInput
from django import forms
from note.models import Note

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['start_date', 'start_time', 'start_datetime', 'start_month', 'start_year']
        widgets = {
            'start_date': DatePickerInput(),
            'start_time': TimePickerInput(),
            'start_datetime': DateTimePickerInput(),
            'start_month': MonthPickerInput(),
            'start_year': YearPickerInput(),
        }