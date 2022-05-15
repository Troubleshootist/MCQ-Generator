from django import forms
import mcq_gen.services as services
from .models import *


class QuestionsFilterForm(forms.Form):
    training = forms.ModelChoiceField(queryset=services.get_all_trainings(
    ), initial=0, widget=forms.Select(attrs={"class": "form-select"}))


class CreateNewQuestionForm(forms.Form):
    training = forms.ModelChoiceField(queryset=services.get_all_trainings(
    ), initial=0, widget=forms.Select(attrs={"class": "form-select"}))
    ata = forms.ModelChoiceField(queryset=services.get_all_atas(), initial=0, widget=forms.Select(
        attrs={"class": "form-select"}), label='ATA Chapter', to_field_name="ata_digit")
    level = forms.ChoiceField(choices=(
        (1, 1),
        (2, 2),
        (3, 3)
    ), label='Level')
    question = forms.CharField(widget=forms.Textarea(
        attrs={'rows': '2', 'cols': '60'}), label='Question')
    answer_a = forms.CharField(widget=forms.Textarea(
        attrs={'rows': '2', 'cols': '60'}), label='Answer A')
    answer_b = forms.CharField(widget=forms.Textarea(
        attrs={'rows': '2', 'cols': '60'}), label='Answer B')
    answer_c = forms.CharField(widget=forms.Textarea(
        attrs={'rows': '2', 'cols': '60'}), label='Answer C')
    correct_answer = forms.ChoiceField(
        choices=(
            ('A', 'A'),
            ('B', 'B'),
            ('C', 'C')
        ), label='Correct Answer')
    book_page = forms.CharField(label='Book Page')
    issued_by = forms.CharField(label='Issued By')


class EditQuestionForm(CreateNewQuestionForm):

    changed_by = forms.CharField(label='Changed By')
    change_reason = forms.CharField(label='Change Reason')
    issued_by = None  # это поле нам не нужно


class CreateExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['date', 'course', 'ata_chapters', 'note_for_examiner']
        widgets = {
            'ata_chapters': forms.CheckboxSelectMultiple(attrs={'class': 'col'}),
            'date': forms.widgets.DateInput(attrs={'type': 'date'})
        }

# class CreateExamForm(forms.Form):
#     date = forms.DateField(widget=forms.SelectDateWidget)
#     course = forms.ModelChoiceField(queryset=services.get_all_courses(
#     ), initial=0, widget=forms.Select(attrs={"class": "form-select"}))
#     note_for_examiner = forms.CharField(
#         label='Note for examiner')
#     ata = forms.ModelChoiceField(queryset=services.get_all_atas(),
#                                  widget=forms.MultipleChoiceField)


class CreateReexamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['date', 'note_for_examiner']
        widgets = {
            'date': forms.widgets.DateInput(attrs={'type': 'date'})
        }
