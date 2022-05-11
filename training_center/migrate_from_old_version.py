
from training_center.wsgi import *
import json
import os
import django
import mcq_gen.models as models
import mcq_gen.old_models as old_models
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'training_center.settings')
django.setup()


def questions_migrate():

    models.Answer.objects.all().delete()
    models.Question.objects.all().delete()

    old_questions = old_models.session.query(old_models.Question).all()
    for old_question in old_questions:
        question = models.Question()
        question.id = old_question.id
        question.question = old_question.question
        try:
            question.level = int(old_question.level)
        except:
            question.level = 0
        question.enabled = old_question.enabled
        question.checked = old_question.checked
        if len(old_question.ataDigit) == 1:
            old_question.ataDigit = '0' + old_question.ataDigit
        ata_chapter = models.AtaChapter.objects.filter(
            ata_digit=old_question.ataDigit).first()
        if not ata_chapter:
            ata_chapter = models.AtaChapter(
                ata_digit=old_question.ataDigit, ata_description='FILL ME!!!')
            ata_chapter.save()
        question.ata_chapter = ata_chapter

        old_training = old_models.session.query(
            old_models.Training).filter_by(id=old_question.training_id).first()
        training = models.Training.objects.filter(
            name=old_training.name).first()
        if not training:
            training = models.Training(name=old_training.name)
            training.save()
        question.training = training

        question.book_page = old_question.book_page
        question.issue_date = old_question.issue_date
        question.check_date = old_question.check_date
        question.change_date = old_question.change_date
        question.ref_to_old_id = old_question.ref_to_old_id
        question.ref_to_new_id = old_question.ref_to_new_id
        question.issued_by = old_question.issued_by
        question.checked_by = old_question.checked_by
        question.changed_by = old_question.changed_by
        question.disable_reason = old_question.disable_reason

        question.save()

        answers = old_question.answers

        old_answer_a = answers[0]
        answer_a = models.Answer(
            question=question, answer=old_answer_a.answer, correct=old_answer_a.correct)

        old_answer_b = answers[1]
        answer_b = models.Answer(
            question=question, answer=old_answer_b.answer, correct=old_answer_b.correct)

        old_answer_c = answers[2]
        answer_c = models.Answer(
            question=question, answer=old_answer_c.answer, correct=old_answer_c.correct)

        question.answers.add(answer_a, bulk=False)
        question.answers.add(answer_b, bulk=False)
        question.answers.add(answer_c, bulk=False)
        answer_a.save()
        answer_b.save()
        answer_c.save()
        print(question)


def ata_migrate(json_file):
    with open(json_file) as f:
        data = json.load(f)
    data_to_db = []
    for item in data:
        ata_obj = models.AtaChapter(
            ata_digit=item['ata_digit'],
            ata_description=item['description']
        )
        data_to_db.append(ata_obj)
    models.AtaChapter.objects.bulk_create(data_to_db)


def course_migrate():

    models.Course.objects.all().delete()
    models.Student.objects.all().delete()
    models.Exam.objects.all().delete()

    old_courses = old_models.session.query(old_models.Course).all()
    courses = []
    for old_course in old_courses:
        old_training = old_models.session.query(
            old_models.Training).filter_by(id=old_course.training_id).first()
        training = models.Training.objects.filter(
            name=old_training.name).first()
        course = models.Course(
            id=old_course.id,
            training=training,
            course_number=old_course.course_number_vdtm
        )
        course.save()
        for old_student in old_course.students.all():
            student = models.Student(
                name=old_student.name,
                surname=old_student.surname,
                dob=old_student.dob
            )
            course.students.add(student, bulk=False)
            student.save()

        for old_exam in old_course.exams.all():
            ata_chapters_query_set = models.AtaChapter.objects.filter(
                ata_digit__in=old_exam.ata_chapters.split('; ')).all()
            exam = models.Exam(
                id=old_exam.id,
                date=old_exam.date,
                is_reexam=old_exam.is_reexam,
                note_for_examiner=old_exam.note_for_examiner
            )
            course.exams.add(exam, bulk=False)
            exam.save()
            for ata_chapter in ata_chapters_query_set:
                exam.ata_chapters.add(ata_chapter)

            for old_exam_question in old_exam.questions.all():
                question = models.Question.objects.filter(
                    id=old_exam_question.question_id).first()
                exam_question = models.ExamQuestion(
                    id=old_exam_question.id,
                    question=question,
                    sequence_number=old_exam_question.seq_number
                )
                exam.exam_questions.add(exam_question, bulk=False)
                exam_question.save()
            print(exam)


def requirements_migrate():
    models.Requirements.objects.all().delete()
    cafs = old_models.session.query(old_models.CAF).all()
    for caf in cafs:
        training_name = old_models.session.query(
            old_models.Training).filter_by(id=caf.training_id).first().name
        training = models.Training.objects.filter(name=training_name).first()

        if len(caf.ata_digit) == 1:
            caf.ata_digit = '0' + caf.ata_digit
        ata_chapter = models.AtaChapter.objects.filter(
            ata_digit=caf.ata_digit).first()
        requirement = models.Requirements(
            training=training,
            ata=ata_chapter,
            questions_number=caf.questions_number,
            level=caf.level
        )
        requirement.save()


def fill_sequence_table():
    all_exam_questions = old_models.session.query(
        old_models.ExamQuestion).all()
    sequence_list = []
    for exam_question in all_exam_questions:
        question = models.Question.objects.filter(
            id=exam_question.id).first()
        exam = models.Exam.objects.filter(id=exam_question.exam_id).first()
        sequence_number = exam_question.seq_number

        sequence = models.QuestionSequence(sequence_number=sequence_number)
        sequence.save()
        sequence.question.set([question])
        sequence.exam.set([exam])
        sequence_list.append([sequence])


def fill_exam_questions_new_table():

    all_exams = models.Exam.objects.all()
    for exam in all_exams:
        qlist = list(exam.exam_questions.values_list(
            'question_id', flat=True).all())
        questions = models.Question.objects.filter(id__in=qlist)
        exam.questions.set(questions)


def fill_sequence_numbers():
    all_exams = models.Exam.objects.all()
    for exam in all_exams:
        old_exam_questions = old_models.session.query(
            old_models.ExamQuestion).filter_by(exam_id=exam.id).all()
        for exam_question in old_exam_questions:
            question = models.Question.objects.filter(
                id=exam_question.question_id).first()
            seq = models.QuestionSequence(
                sequence_number=exam_question.seq_number)
            seq.save()
            seq.exam.add(exam)
            seq.question.add(question)


def migrate_results():
    old_results = old_models.session.query(old_models.QuestionResult).all()
    for old_result in old_results:
        exam = models.Exam.objects.filter(id=old_result.exam_id).first()
        question = models.Question.objects.filter(
            id=old_result.question_id).first()
        student = models.Student.objects.filter(
            id=old_result.student_id).first()
        result = models.QuestionResult(is_correct=old_result.correct)
        result.save()
        result.exam.add(exam)
        result.question.add(question)
        result.student.add(student)
        print(result)


def migrate_exam_questions():
    old_exam_questions = old_models.session.query(
        old_models.ExamQuestion).all()

    for old_exam_question in old_exam_questions:
        exam = models.Exam.objects.filter(id=old_exam_question.exam_id).first()
        question = models.Question.objects.filter(
            id=old_exam_question.question_id).first()
        exam.questions.add(question)
        sequence = models.QuestionSequence(
            sequence_number=old_exam_question.seq_number)
        sequence.exam = exam
        sequence.question = question
        sequence.save()


if __name__ == '__main__':

    # questions_migrate()
    # ata_migrate('/Users/dmitriy/Desktop/CAF.json')
    # course_migrate()
    # requirements_migrate()
    # fill_sequence_table()
    # fill_exam_questions_new_table()
    # fill_sequence_numbers()
    # migrate_results()
    migrate_exam_questions()
    pass
