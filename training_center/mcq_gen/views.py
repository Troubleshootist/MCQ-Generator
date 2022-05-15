from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import json
from . import services
from .forms import *


def questions_database(request):
    filter_form = QuestionsFilterForm()
    context = {
        "trainings": services.get_all_trainings(),
        "atas": services.get_all_atas(),
        "filter_form": filter_form
    }
    if request.method == "POST":
        atas_list = []
        # training = Training.objects.filter(id=request.POST['training']).first()
        training_id = request.POST['training']
        for item in request.POST:
            if item != 'csrfmiddlewaretoken' and item != 'training':
                atas_list.append(item)
        if len(atas_list) > 0:
            questions_html_table, questions_count, training_name = services.get_questions_by_ata_and_training(
                atas_list=atas_list, training_id=training_id)
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
    disabled_question = services.disable_question(question_id=question_id,
                                                  disable_reason=disable_reason)
    return render(request, 'question_details.html', context={"question": disabled_question})


def enable_question(request):
    question_id = request.GET['question_id']
    enabled_by = request.GET['enabled_by']
    enabled_question = services.enable_question(question_id=question_id,
                                                enabled_by=enabled_by)
    return render(request, 'question_details.html', context={"question": enabled_question})


def uncheck_question(request):
    question_id = request.GET['question_id']
    unchecked_question = services.uncheck_question(question_id=question_id)
    return render(request, 'question_details.html', context={"question": unchecked_question})


def check_question(request):
    question_id = request.GET['question_id']
    checked_by = request.GET['checked_by']
    checked_question = services.check_question(question_id=question_id,
                                               checked_by=checked_by)
    return render(request, 'question_details.html', context={"question": checked_question})


def create_question(request):
    create_question_form = CreateNewQuestionForm()
    context = {'form': create_question_form}
    if request.method == 'POST':
        create_question_form = CreateNewQuestionForm(request.POST)
        if create_question_form.is_valid():
            created_question = services.create_edit_question(
                create_question_form.cleaned_data)
            return redirect('question_details', question_id=created_question.id)
    return render(request, 'edit_question.html', context)


def edit_question(request, question_id):
    initial = services.get_initial_values_for_question_edit_form(question_id)
    edit_question_form = EditQuestionForm(initial=initial)
    context = {'form': edit_question_form}
    if request.method == 'POST':
        edit_question_form = EditQuestionForm(request.POST)
        if edit_question_form.is_valid():
            edited_question = services.create_edit_question(edit_question_form.cleaned_data,
                                                            old_question_id=question_id)
            return redirect('question_details', question_id=edited_question.id)
    return render(request, 'edit_question.html', context)


def all_exams(request):
    all_exams_html_table = services.get_all_exams_html_table()
    context = {'table': all_exams_html_table}
    return render(request, 'exams.html', context)


def exam_details(request, exam_id):

    exam = services.get_exam_by_id(exam_id)
    is_it_second_reexam = services.is_it_second_reexam(exam)
    is_it_reexam = services.is_it_reexam(exam)
    is_exam_checked = services.is_exam_checked(exam)

    context = {'exam': exam,
               'is_it_reexam': is_it_reexam,
               'is_it_second_reexam': is_it_second_reexam,
               'is_exam_checked': is_exam_checked}
    return render(request, 'exam_details.html', context)


def ajax_details_for_questions(request, exam_id):
    exam_questions_details_json = services.get_exam_details(exam_id)
    return JsonResponse(exam_questions_details_json['exam_details'])


def ajax_count_questions_by_ata(request, exam_id):
    count_questions_by_ata_json = services.get_exam_details(exam_id)
    return JsonResponse(count_questions_by_ata_json['exam_questions_by_ata'])


def create_exam(request):
    create_exam_form = CreateExamForm()
    context = {'create_exam_form': create_exam_form,
               'atas': services.get_all_atas}
    if request.method == 'POST':
        create_exam_form = CreateExamForm(request.POST)
        if create_exam_form.is_valid():
            created_exam = services.create_exam(create_exam_form.cleaned_data)
            return redirect('exam_details', exam_id=created_exam.id)
    return render(request, 'create_exam.html', context)


def create_reexam(request, exam_id):
    create_reexam_form = CreateReexamForm()
    context = {'create_reexam_form': create_reexam_form}
    if request.method == 'POST':
        create_reexam_form = CreateReexamForm(request.POST)
        if create_reexam_form.is_valid():
            created_reexam = services.create_reexam(
                create_reexam_form.cleaned_data, exam_id)
            return redirect('exam_details', exam_id=created_reexam.id)

    return render(request, 'create_reexam.html', context)


def delete_exam(request, exam_id):

    services.delete_exam(exam_id)
    return redirect('all_exams')


def auto_change_question(request, exam_id):

    exam = services.get_exam_by_id(exam_id=exam_id)
    question_id_to_change = json.loads(request.GET['question'])[1]
    changed_exam = services.change_one_question_in_exam(
        exam, question_id_to_change)

    return JsonResponse(changed_exam, safe=False)


def all_courses(request):

    courses = services.get_all_courses()
    context = {'courses': courses}

    return render(request, 'courses.html', context)


def course_power_json(request, course_id):
    power = services.get_course_power(course_id)
    return JsonResponse({'power': power})
