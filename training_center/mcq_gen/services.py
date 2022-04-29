import pandas as pd


from .models import *

def get_questions_database():
    questions = Question.objects.all()
    return questions

def get_all_trainings():
    return Training.objects.all()

def get_all_atas():
    return AtaChapter.objects.order_by('ata_digit')

def get_question_by_id(question_id):

    question = Question.objects.filter(id=question_id).first()
    return question

def get_questions_by_ata_and_training(atas_list, training_id):
    training = Training.objects.filter(id=training_id).first()
    atas = AtaChapter.objects.filter(ata_digit__in = atas_list).values_list('id', flat=True)
    questions_queryset = Question.objects.filter(ata_chapter__in = atas, training=training).all()
    questions_count = len(questions_queryset)
    df = pd.DataFrame(list(questions_queryset.values()))
    if not df.empty:
        df = df.drop(columns=['training_id', 
                              'ata_chapter_id', 
                              'issued_by', 
                              'checked_by', 
                              'changed_by',
                              'ref_to_old_id',
                              'ref_to_new_id'])
        df = df.replace(to_replace=True, value='Yes')
        df = df.replace(to_replace=False, value='No')
        return df.to_html(classes='table table-sm table-hover table-bordered', table_id='questions_database'), questions_count, training.name
    else:
        return '', 0, training.name

def disable_question(question_id, disable_reason):
    question = Question.objects.filter(id=question_id).first()
    question.disable_reason = disable_reason
    question.enabled = False
    question.save()
    return question

def enable_question(question_id, enabled_by):
    question = Question.objects.filter(id=question_id).first()
    question.enabled = True
    question.enabled_by = enabled_by
    question.save()
    return question

def uncheck_question(question_id):
    question = Question.objects.filter(id=question_id).first()
    question.checked = False
    question.save()
    return question

def check_question(question_id, checked_by):
    question = Question.objects.filter(id=question_id).first()
    question.checked = True
    question.checked_by = checked_by
    question.save()
    return question

    
