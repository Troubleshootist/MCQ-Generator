from numpy import expand_dims
from math import ceil
from django.db.models import Q
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
    atas = AtaChapter.objects.filter(
        ata_digit__in=atas_list).values_list('id', flat=True)
    questions_queryset = Question.objects.filter(
        ata_chapter__in=atas, training=training).all()
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


def create_edit_question(data, old_question_id=None):
    new_question = Question(
        training=data['training'],
        ata_chapter=data['ata'],
        level=data['level'],
        question=data['question'],
        book_page=data['book_page'],
        issue_date=date.today()
    )

    if old_question_id:  # если меняем вопрос, то передаем ид старого вопроса
        old_question = Question.objects.filter(
            id=old_question_id).first()
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
        new_question.issued_by = data['issued_by']
        new_question.save()

    answer_a = Answer(answer=data['answer_a'])
    answer_b = Answer(answer=data['answer_b'])
    answer_c = Answer(answer=data['answer_c'])

    if data['correct_answer'] == 'A':
        answer_a.correct = True
    elif data['correct_answer'] == 'B':
        answer_b.correct = True
    elif data['correct_answer'] == 'C':
        answer_c.correct = True
    new_question.answers.add(answer_a, bulk=False)
    new_question.answers.add(answer_b, bulk=False)
    new_question.answers.add(answer_c, bulk=False)
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


def create_exam(data):

    # Определяем пересдача ли или нет
    exam = Exam(
        date=data['date'],
        note_for_examiner=data['note_for_examiner'],
        course=data['course'])
    pre_exam = exam.course.exams.filter(
        ata_chapters__in=data['ata_chapters'], course=data['course']).last()
    if pre_exam:
        reexam(exam=exam, pre_exam=pre_exam)
    else:
        exam.save()
        exam.ata_chapters.set(data['ata_chapters'])
        new_exam(exam)


def new_exam(exam):
    requirements = Requirements.objects.filter(
        training=exam.course.training, ata__in=exam.ata_chapters.all())
    for requirement in requirements:
        questions_to_exam = Question.objects.filter(
            ata_chapter=requirement.ata,
            training=exam.course.training,
            level=requirement.level
        ).order_by('?').all()[:requirement.questions_number]
        _add_questions_to_exam(exam, questions_to_exam)

    remainder_of_div_by_four = exam.questions.count() % 4
    if remainder_of_div_by_four != 0:
        questions_number_to_add = 4 - remainder_of_div_by_four
        questions_to_exam = Question.objects.filter(
            ~Q(id__in=exam.questions.all()),
            ata_chapter__in=exam.ata_chapters.all(),
            training=exam.course.training
        ).order_by('?').all()[:questions_number_to_add]
        _add_questions_to_exam(exam, questions_to_exam)

    set_exam_questions_sequence(exam)
    return exam


def create_reexam(data, exam_id):
    initial_exam = get_exam_by_id(exam_id)
    exam = Exam(
        date=data['date'],
        note_for_examiner=data['note_for_examiner'],
        course=initial_exam.course)
    exam.save()
    exam.ata_chapters.set(initial_exam.ata_chapters.all())
    _fill_questions_for_reexam(exam, initial_exam)
    set_exam_questions_sequence(exam=exam, initial_exam=initial_exam)

    return exam


def _fill_questions_for_reexam(exam, initial_exam):
    requirements = Requirements.objects.filter(
        training=exam.course.training, ata__in=exam.ata_chapters.all())
    for requirement in requirements:
        not_used_count = ceil(requirement.questions_number*50/100)
        used_count_max = requirement.questions_number - not_used_count

        not_used_questions_in_inital_exam, used_questions_in_initial_exam = \
            _get_questions_queryset_for_exact_requirement(
                requirement, used_count_max, not_used_count, initial_exam, exam)

        while (not_used_questions_in_inital_exam.count() + used_questions_in_initial_exam.count() < requirement.questions_number):
            not_used_count += 1
            used_count_max += 1
            not_used_questions_in_inital_exam, used_questions_in_initial_exam = \
                _get_questions_queryset_for_exact_requirement(
                    requirement, used_count_max, not_used_count, initial_exam, exam)

        _add_questions_to_exam(
            exam, not_used_questions_in_inital_exam.all())
        _add_questions_to_exam(exam, used_questions_in_initial_exam.all())

    return exam


def _get_questions_queryset_for_exact_requirement(requirement, used_count_max, not_used_count, initial_exam, exam):

    not_used_questions_in_inital_exam = Question.objects.filter(
        ~Q(id__in=initial_exam.questions.all()),
        ata_chapter=requirement.ata,
        training=exam.course.training,
        level=requirement.level
    ).order_by('?')[:not_used_count]

    used_questions_in_initial_exam = Question.objects.filter(
        id__in=initial_exam.questions.all(),
        ata_chapter=requirement.ata,
        training=exam.course.training,
        level=requirement.level
    ).order_by('?')[:used_count_max]

    return not_used_questions_in_inital_exam, used_questions_in_initial_exam


def _add_questions_to_exam(exam, questions_queryset):
    for question in questions_queryset:
        exam.questions.add(question)


def reexam(exam, pre_exam):
    pass


def set_exam_questions_sequence(exam, initial_exam=None):
    while not _is_sequence_ok(exam=exam, initial_exam=initial_exam):
        QuestionSequence.objects.filter(exam=exam).delete()
        shuffled_exam_questions = exam.questions.order_by(
            'ata_chapter', '?').all()
        for i, question in enumerate(shuffled_exam_questions):
            i += 1
            sequence = QuestionSequence(sequence_number=i)
            sequence.save()
            sequence.question.add(question)
            sequence.exam.add(exam)


def _is_sequence_ok(exam, initial_exam=None):

    if _is_questions_for_pre_exam_has_not_same_sequence(exam, initial_exam) \
            and _is_exam_has_not_null_sequence(exam) \
            and _is_continuity_ok(exam):
        return True
    else:
        return False


def _is_exam_has_not_null_sequence(exam):
    sequences = QuestionSequence.objects.filter(exam=exam).count()
    if sequences != exam.questions.count():
        return False
    else:
        return True


def _is_questions_for_pre_exam_has_not_same_sequence(exam, initial_exam):
    if not initial_exam:
        return True
    for question in exam.questions.all():
        exam_sequences = QuestionSequence.objects.filter(
            question=question, exam__in=[exam, initial_exam])
        if exam_sequences.count() > 1:
            if exam_sequences.all()[0].sequence_number == exam_sequences.all()[1].sequence_number:
                return False
    return True


def _is_continuity_ok(exam):
    """"Проверяет порядок следоваеия вопросов 1 2 3 4  .... n"""
    sequence_queryset = QuestionSequence.objects.filter(
        exam=exam).order_by('sequence_number').all()
    questions_count = len(sequence_queryset)

    if sequence_queryset.first().sequence_number != 1:
        return False

    i = 0
    while i <= questions_count:
        if i < (questions_count - 1):
            if (sequence_queryset[i + 1].sequence_number - sequence_queryset[i].sequence_number) != 1:
                # print('order plohoi')
                return False
        if i == (questions_count - 1):
            if sequence_queryset[i].sequence_number - sequence_queryset[i - 1].sequence_number != 1:
                print('order plohoi')
                return False
        i += 1

    return True


def get_all_exams_html_table():
    all_exams_queryset = Exam.objects.values()
    df = pd.DataFrame(list(all_exams_queryset))
    return df.to_html(classes='table table-sm table-hover table-bordered', table_id='exams_database')


def get_exam_details_html_table(exam_id):
    exam = get_exam_by_id(exam_id)
    df = pd.DataFrame(list(exam.questions.values()))
    return df.to_html(classes='table table-sm table-hover table-bordered', table_id='exams_details')


def get_all_courses():
    return Course.objects.all()


def get_ata_names_from_exam(exam_id):
    exam = get_exam_by_id(id=exam_id)
    return exam.ata_chapters.all().values('ata_digit')


def get_exam_by_id(exam_id):
    return Exam.objects.filter(id=exam_id).first()


if __name__ == '__main__':
    pass
