import os

from .models import *

def get_questions_database():
    questions = Question.objects.all()
    return questions

def get_all_trainings():
    return Training.objects.all()

def get_all_atas():
    return AtaChapter.objects.order_by('ata_digit')
    
