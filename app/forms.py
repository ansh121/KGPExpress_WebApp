from django import forms
from django.forms import ModelForm, DateInput
from app.models import Event
from datetime import datetime, timedelta, date
from authentication.models import CustomUser

class SearchForm(forms.Form):
    subject = forms.CharField()
    semester = forms.CharField()
    year = forms.DecimalField()

class EventForm(ModelForm):
    event_name = forms.CharField
    start_time = forms.DateTimeField(widget = DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'))
    end_time = forms.DateTimeField(widget = DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'))
    description = forms.CharField
    is_recurring = forms.BooleanField()
    type = forms.CharField
    #time_of_edit = forms.DateTimeField(widget=DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'))

    class Meta:
        model = Event
        # datetime-local is a HTML5 input type, format to make date time show on fields
        fields = ('event_name','start_time','end_time','description','is_recurring','type')

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        # input_formats parses HTML5 datetime-local input to datetime field
        self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)