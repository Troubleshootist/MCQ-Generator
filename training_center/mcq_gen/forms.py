from django import forms
from .services import get_all_trainings, get_all_atas
from .models import *

class QuestionsFilterForm(forms.Form):
    training = forms.ModelChoiceField(queryset=get_all_trainings(), initial=0, widget=forms.Select(attrs={"class": "form-select"}))
    # ata = forms.ModelMultipleChoiceField(queryset=get_all_atas(), initial=0, widget=forms.CheckboxSelectMultiple(attrs={"class":"column"}))