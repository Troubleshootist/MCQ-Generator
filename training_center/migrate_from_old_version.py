import os
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'training_center.settings')
import django
django.setup()
import mcq_gen.models as models
import mcq_gen.old_models as old_models





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
            question.level = None
        question.enabled = old_question.enabled
        question.checked = old_question.checked
        if len(old_question.ataDigit) == 1:
            old_question.ataDigit = '0' + old_question.ataDigit
        ata_chapter = models.AtaChapter.objects.filter(ata_digit=old_question.ataDigit).first()
        if not ata_chapter:
            ata_chapter = models.AtaChapter(ata_digit=old_question.ataDigit, ata_description='FILL ME!!!')
            ata_chapter.save()
        question.ata_chapter = ata_chapter

        old_training = old_models.session.query(old_models.Training).filter_by(id = old_question.training_id).first()
        training = models.Training.objects.filter(name=old_training.name).first()
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
        answer_a = models.Answer(question=question, answer=old_answer_a.answer, correct=old_answer_a.correct)      
        
        
        old_answer_b = answers[1]
        answer_b = models.Answer(question=question, answer=old_answer_b.answer, correct=old_answer_b.correct)      
        
        
        old_answer_c = answers[2]
        answer_c = models.Answer(question=question, answer=old_answer_c.answer, correct=old_answer_c.correct)      
        

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
    


if __name__ == '__main__':
    questions_migrate()
    # ata_migrate('/Users/dmitriy/Desktop/CAF.json')


    pass