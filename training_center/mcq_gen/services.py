import pandas as pd
from datetime import date
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

def create_edit_question(data, old_question_id = None):
    new_question = Question(
        training = data['training'],
        ata_chapter = data['ata'],
        level = data['level'],
        question = data['question'],
        book_page = data['book_page'],
        issue_date = date.today()
    )

    if old_question_id: # если меняем вопрос, то передаем ид старого вопроса
        old_question = Question.objects.filter(id=old_question_id).first()
        new_question.ref_to_old_id = old_question.id
        new_question.issued_by = data['changed_by']
        new_question.save()
        old_question.enabled = False
        old_question.changed_by = data['changed_by']
        old_question.disable_reason = data['change_reason']
        old_question.ref_to_new_id = new_question.id
        old_question.change_date = date.today()
        old_question.save()
    else:
        issued_by = data['issued_by']
        new_question.save()

    answer_a = Answer(answer = data['answer_a'])
    answer_b = Answer(answer = data['answer_b'])
    answer_c = Answer(answer = data['answer_c'])

    if data['correct_answer'] == 'A':
        answer_a.correct = True
    elif data['correct_answer'] == 'B':
        answer_b.correct = True
    elif data['correct_answer'] == 'C':
        answer_c.correct = True
    new_question.answers.add(answer_a, bulk =False)
    new_question.answers.add(answer_b, bulk =False)
    new_question.answers.add(answer_c, bulk =False)
    answer_a.save()
    answer_b.save()
    answer_c.save()

    return new_question

def get_initial_values_for_question_edit_form(question_id):
    question = Question.objects.filter(id=question_id).first()
    if question.answers.all()[0].correct:
        correct_answer_char = 'A'
    elif question.answers.all()[1].correct:
        correct_answer_char = 'B'
    elif question.answers.all()[2].correct:
        correct_answer_char = 'C'

    initial_values_for_form = {
        'training': question.training,
        'ata': question.ata_chapter,
        'level': question.level,
        'question': question.question,
        'answer_a': question.answers.all()[0].answer,
        'answer_b': question.answers.all()[1].answer,
        'answer_c': question.answers.all()[2].answer,
        'correct_answer': correct_answer_char,
        'book_page': question.book_page,
    }
    return initial_values_for_form

    





    
