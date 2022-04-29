from django.urls import path

from . import views

urlpatterns = [
    path('questions_database/', views.questions_database, name='questions_database'),
    path('questions_database/question_details/<str:question_id>/', views.question_details, name='question_details'),
    path('questions_database/disable_question/', views.disable_question, name='disable_question'),
    path('questions_database/enable_question/', views.enable_question, name='enable_question'),
    path('questions_database/uncheck_question/', views.uncheck_question, name='uncheck_question'),
    path('questions_database/check_question/', views.check_question, name='check_question'),
    path('test/', views.test, name='my_ajax_url'),
]