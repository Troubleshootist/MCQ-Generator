from django.shortcuts import render, redirect
from django.core import serializers
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic import ListView, UpdateView, CreateView, DeleteView
import json
from . import services
from .forms import *


class AtaChaptersListView(ListView):

    model = services.AtaChapter


class AtaChapterUpdateView(UpdateView):
    model = services.AtaChapter
    fields = ['ata_digit', 'ata_description']
    success_url = reverse_lazy('atas_list')


class AtaChapterCreateView(CreateView):
    model = services.AtaChapter
    fields = '__all__'
    success_url = reverse_lazy('atas_list')


class AtaChapterDeleteView(DeleteView):
    model = services.AtaChapter
    success_url = reverse_lazy('atas_list')


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


def get_questions_by_ata_and_training(request):
    training_name = request.GET.get('training_name')
    atas = request.GET.getlist('atas')
    filtered_info = services.get_questions_by_ata_and_training_name(
        atas, training_name)
    return JsonResponse(filtered_info, safe=False)


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
               'atas': services.get_all_atas,
               'courses': services.get_all_courses()}
    if request.method == 'POST':
        create_exam_form = CreateExamForm(request.POST)
        if create_exam_form.is_valid():
            created_exam = services.create_exam(create_exam_form.cleaned_data)
            return redirect('exam_details', exam_id=created_exam.id)
    return render(request, 'create_exam.html', context)


def get_remaining_atas_for_course(request, course_id):
    remaining_ata_chapters = services.get_remaining_atas_for_course(
        course_id)
    context = {'remaining_ata_chapters': remaining_ata_chapters}
    return JsonResponse(context)


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


def course_details(request, course_id):
    course = services.get_course_by_id(course_id)
    context = {
        'students': services.course_details(course)['student_stats'],
        'course': course,
        'exams': services.get_course_exams_details(course),
        'power': services.get_course_power(course_id)
    }
    return render(request, 'course_details.html', context)


def create_course(request):
    create_course_form = CreateCourseForm()
    if request.method == 'POST':
        create_course_form = CreateCourseForm(request.POST)
        if create_course_form.is_valid():
            new_course = create_course_form.save()
            return redirect('course_details', new_course.id)
    context = {'create_course_form': create_course_form}
    return render(request, 'create_course.html', context)


def add_student_to_course(request, course_id):
    course = services.get_course_by_id(course_id)
    create_student_form = CreateStudentForm()
    if request.method == 'POST':
        create_student_form = CreateStudentForm(request.POST)
        if create_student_form.is_valid():
            new_student = create_student_form.save()
            new_student.course = course
    context = {'create_student_form': create_student_form}
    return render(request, 'create_student.html', context)


def manage_students(request, course_id):
    course = services.get_course_by_id(course_id)
    students = course.students.all()
    context = {
        'students': students,
        'course': course
    }
    return render(request, 'students_list.html', context)


def student_update(request, course_id, student_id=0):
    """Update or create student"""

    course = services.get_course_by_id(course_id)

    if request.method == 'GET':
        if student_id == 0:
            student_form = StudentForm()
        else:
            student = services.get_student_by_id(student_id)
            student_form = StudentForm(instance=student)
        context = {'student_form': student_form}
        return render(request, 'student_update.html', context)
    else:
        if student_id == 0:
            student_form = StudentForm(request.POST)
        else:
            student = services.get_student_by_id(student_id)
            student_form = StudentForm(request.POST, instance=student)
        if student_form.is_valid():

            if student_form.instance.course_id is None:
                student_form.instance.course_id = course.id
            student_form.save()

        return redirect('manage_students', course_id=course_id)


def student_delete(request, course_id, student_id):
    services.student_delete(student_id)
    return redirect('manage_students', course_id)


def trainings(request):
    context = {
        'trainings': services.get_all_trainings()
    }
    return render(request, 'trainings.html', context)


def training_details(request, training_id):
    training = services.get_training_by_id(training_id)
    context = {
        'training': training
    }
    return render(request, 'training_details.html', context)


def requirement_update(request, training_id, requirement_id=0):
    training = services.get_training_by_id(training_id)
    if request.method == 'GET':
        if requirement_id == 0:
            requirement_form = RequirementForm()
        else:
            requirement = services.get_requirement_by_id(requirement_id)
            requirement_form = RequirementForm(instance=requirement)
        context = {'requirement_form': requirement_form}
        return render(request, 'requirement_update.html', context)
    else:
        if requirement_id == 0:
            requirement_form = RequirementForm(request.POST)
        else:
            requirement = services.get_requirement_by_id(requirement_id)
            requirement_form = RequirementForm(
                request.POST, instance=requirement)

        if requirement_form.is_valid():
            if requirement_form.instance.training_id is None:
                requirement_form.instance.training_id = training.id
            requirement_form.save()

    return redirect('training_details', training.id)


def requirement_delete(request, training_id, requirement_id):
    services.delete_requirement(requirement_id)
    return redirect('training_details', training_id)
