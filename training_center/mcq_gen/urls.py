from django.urls import path

from . import views

urlpatterns = [
    path('questions_database/', views.questions_database,
         name='questions_database'),
    path('get_questions_by_ata_and_training', views.get_questions_by_ata_and_training,
         name='get_questions_by_ata_and_training'),
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
    path('exams/create/<int:course_id>/get_remaining_atas_for_course',
         views.get_remaining_atas_for_course, name='get_remaining_atas_for_course'),
    path('exams/<int:exam_id>/create_reexam',
         views.create_reexam, name='create_reexam'),
    path('exams/<int:exam_id>/delete_exam',
         views.delete_exam, name='delete_exam'),

    path('exams/<int:exam_id>/auto_change_questions',
         views.auto_change_question, name='auto_change_questions'),

    path('courses/', views.all_courses, name='all_courses'),
    path('courses/<int:course_id>/details',
         views.course_details, name='course_details'),
    path('courses/create', views.create_course, name='create_course'),

    path('courses/<int:course_id>/manage_students',
         views.manage_students, name='manage_students'),
    path('courses/<int:course_id>/manage_students/<int:student_id>/student_update',
         views.student_update, name='student_update'),
    path('courses/<int:course_id>/manage_students/<int:student_id>/student_delete',
         views.student_delete, name='student_delete'),
    path('courses/<int:course_id>/manage_students/student_create',
         views.student_update, name='student_create'),

    path('trainings', views.trainings, name='trainings'),
    path('trainings/<int:training_id>/details',
         views.training_details, name='training_details'),

    path('trainings/<int:training_id>/details/<int:requirement_id>/requirement_update',
         views.requirement_update, name='requirement_update'),
    path('trainings/<int:training_id>/details/<int:requirement_id>/requirement_delete',
         views.requirement_delete, name='requirement_delete'),
    path('trainings/<int:training_id>/details/requirement_create',
         views.requirement_update, name='requirement_create'),

    path('atas/', views.AtaChaptersListView.as_view(), name='atas_list'),
    path('atas/create', views.AtaChapterCreateView.as_view(), name='ata_create'),
    path('atas/<pk>/update', views.AtaChapterUpdateView.as_view(), name='ata_update'),
    path('atas/<pk>/delete', views.AtaChapterDeleteView.as_view(), name='ata_delete')
]
