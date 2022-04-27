from django.urls import path

from . import views

urlpatterns = [
    path('questions_database/', views.questions_database)
]