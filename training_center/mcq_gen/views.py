from django.shortcuts import render
from . import services
from .forms import QuestionsFilterForm



def questions_database(request):
    filter_form = QuestionsFilterForm()
    context = {
        "questions": services.get_questions_database(),
        "trainings": services.get_all_trainings(),
        "atas": services.get_all_atas(),
        "filter_form": filter_form
    }
    return render(request, 'test.html', context)