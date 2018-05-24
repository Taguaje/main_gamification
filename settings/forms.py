from django import forms
from .models import LMS


class LMSChangeNameForm(forms.ModelForm):
    class Meta:
        model = LMS
        fields = {'Name'}


class LMSCreateForm(forms.ModelForm):
    class Meta:
        model = LMS
        fields = {'Name', 'PointsIsOn', 'MaxPoints'}
