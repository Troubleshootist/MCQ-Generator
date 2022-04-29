from django.shortcuts import render
from django.views.generic import ListView
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from . import services
from .forms import QuestionsFilterForm




def questions_database(request):
    filter_form = QuestionsFilterForm()
    context = {
        "trainings": services.get_all_trainings(),
        "atas": services.get_all_atas(),
        "filter_form": filter_form
    }
    if request.method=="POST":
        atas_list = []
        # training = Training.objects.filter(id=request.POST['training']).first() 
        training_id = request.POST['training']
        for item in request.POST:
            if item != 'csrfmiddlewaretoken' and item != 'training':
                atas_list.append(item)
        if len(atas_list) > 0:
            questions_html_table, questions_count, training_name = services.get_questions_by_ata_and_training(atas_list=atas_list, training_id = training_id)
            context['questions_table'] = questions_html_table
            context['questions_count'] = questions_count
            context['training_name'] = training_name
            context['atas_list'] = ', '.join(atas_list)
        else:
            context['questions_table'] = ''
        return render(request, 'questions_database.html', context)
    return render(request, 'questions_database.html', context)

def test(request):
    questions_queryset = services.get_questions_database()
    json = serializers.serialize('json', questions_queryset)
    print(json)
    return HttpResponse(json, content_type='application/json')


def question_details(request, question_id):
    question = services.get_question_by_id(question_id)

    return render(request, 'question_details.html', context={"question": question})


def disable_question(request):
    question_id = request.GET['question_id']
    disable_reason = request.GET['disable_reason']
    disabled_question = services.disable_question(question_id = question_id, 
                                                  disable_reason=disable_reason)
    return render(request, 'question_details.html', context={"question": disabled_question})

def enable_question(request):
    question_id = request.GET['question_id']
    enabled_by = request.GET['enabled_by'] 
    enabled_question = services.enable_question(question_id = question_id, 
                                                enabled_by=enabled_by)
    return render(request, 'question_details.html', context={"question": disabled_question})    

def uncheck_question(request):
    question_id = request.GET['question_id']
    unchecked_question = services.uncheck_question(question_id= question_id)
    return render(request, 'question_details.html', context={"question": unchecked_question})

def check_question(request):
    question_id = request.GET['question_id']
    checked_by = request.GET['checked_by'] 
    checked_question = services.check_question(question_id = question_id, 
                                                checked_by=checked_by)
    return render(request, 'question_details.html', context={"question": checked_question})   