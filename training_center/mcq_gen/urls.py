from django.urls import path

from . import views

urlpatterns = [
    path('questions_database/', views.questions_database,
         name='questions_database'),
    path('questions_database/question_details/<str:question_id>/',
         views.question_details, name='question_details'),
    path('questions_database/question_details/<str:question_id>/edit_question/',
         views.edit_question, name='edit_question'),
    path('questions_database/disable_question/',
         views.disable_question, name='disable_question'),
    path('questions_database/enable_question/',
         views.enable_question, name='enable_question'),
    path('questions_database/uncheck_question/',
         views.uncheck_question, name='uncheck_question'),
    path('questions_database/check_question/',
         views.check_question, name='check_question'),
    path('questions_database/create_question/',
         views.create_question, name='create_question'),

    path('exams/', views.all_exams, name='all_exams'),
    path('exams/<str:exam_id>/details',
         views.exam_details, name='exam_details'),
    path('exams/create_exam/',
         views.create_exam, name='create_exam'),
    path('exams/<str:exam_id>/create_reexam',
         views.create_reexam, name='create_reexam'),
    path('exams/<str:exam_id>/delete_exam',
         views.delete_exam, name='delete_exam'),

    path('exams/<str:exam_id>/auto_change_question',
         views.auto_change_question, name='auto_change_questions')
]
