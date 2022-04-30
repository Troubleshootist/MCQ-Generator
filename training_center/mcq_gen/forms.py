from django import forms
import mcq_gen.services as services
from .models import *

class QuestionsFilterForm(forms.Form):
    training = forms.ModelChoiceField(queryset=services.get_all_trainings(), initial=0, widget=forms.Select(attrs={"class": "form-select"}))
    # ata = forms.ModelMultipleChoiceField(queryset=get_all_atas(), initial=0, widget=forms.CheckboxSelectMultiple(attrs={"class":"column"}))

class CreateQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'


class CreateNewQuestionForm(forms.Form):
    training = forms.ModelChoiceField(queryset=services.get_all_trainings(), initial=0, widget=forms.Select(attrs={"class": "form-select"}))
    ata = forms.ModelChoiceField(queryset=services.get_all_atas(), initial=0, widget=forms.Select(attrs={"class": "form-select"}), label='ATA Chapter', to_field_name="ata_digit")
    level = forms.ChoiceField(choices=((1,1),(2,2),(3,3)), label='Level')
    question = forms.CharField(widget=forms.Textarea(attrs={'rows':'2', 'cols':'60'}), label='Question')
    answer_a = forms.CharField(widget=forms.Textarea(attrs={'rows':'2', 'cols':'60'}), label='Answer A')
    answer_b = forms.CharField(widget=forms.Textarea(attrs={'rows':'2', 'cols':'60'}), label='Answer B')
    answer_c = forms.CharField(widget=forms.Textarea(attrs={'rows':'2', 'cols':'60'}), label='Answer C')
    correct_answer = forms.ChoiceField(choices=(('A','A'),('B','B'),('C','C')), label='Correct Answer')
    book_page = forms.CharField(label='Book Page')
    issued_by = forms.CharField(label='Issued By')

class EditQuestionForm(CreateNewQuestionForm):
    
    changed_by = forms.CharField(label='Changed By')
    change_reason = forms.CharField(label='Change Reason')
    issued_by = None # это поле нам не нужно

