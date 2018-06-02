from django import forms
from .models import LMS, LMSEvents, EventPoints


class LMSChangeNameForm(forms.ModelForm):
    class Meta:
        model = LMS
        fields = {'Name'}


class LMSCreateForm(forms.ModelForm):
    class Meta:
        model = LMS
        fields = {'Name', 'PointsIsOn', 'MaxPoints'}


class EventForm(forms.ModelForm):
    class Meta:
        model = LMSEvents
        fields = {'name'}
