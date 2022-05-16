from django.urls import path

from . import views

urlpatterns = [
    path('questions_database/', views.questions_database,
         name='questions_database'),
    path('questions_database/question_details/<int:question_id>/',
         views.question_details, name='question_details'),
    path('questions_database/question_details/<int:question_id>/edit_question/',
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
    path('exams/<int:exam_id>/details',
         views.exam_details, name='exam_details'),
    path('exams/<int:exam_id>/ajax_details_for_questions',
         views.ajax_details_for_questions, name='ajax_details_for_questions'),
    path('exams/<int:exam_id>/ajax_count_questions_by_ata',
         views.ajax_count_questions_by_ata, name='ajax_count_questions_by_ata'),
    path('exams/create/',
         views.create_exam, name='create_exam'),
    path('exams/<int:exam_id>/create_reexam',
         views.create_reexam, name='create_reexam'),
    path('exams/<int:exam_id>/delete_exam',
         views.delete_exam, name='delete_exam'),

    path('exams/<int:exam_id>/auto_change_questions',
         views.auto_change_question, name='auto_change_questions'),

    path('courses/', views.all_courses, name='all_courses'),
    path('courses/<int:course_id>/details', views.course_details, name='course_details'),
    path('courses/create', views.create_course, name='create_course'),

    path('courses/<int:course_id>/manage_students', views.manage_students, name='manage_students'),
    path('courses/<int:course_id>/manage_students/<int:student_id>/student_update',
         views.student_update, name='student_update'),
    path('courses/<int:course_id>/manage_students/student_create',
         views.student_update, name='student_create')
]
