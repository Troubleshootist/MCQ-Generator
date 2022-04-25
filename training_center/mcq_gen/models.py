from django.db import models


class Training(models.Model):
    name = models.CharField(max_length=100)

class AtaChapter(models.Model):
    ata_digit = models.CharField(max_length=10)
    ata_description = models.CharField(max_length=100)


class Question(models.Model):
    question = models.CharField(max_length=200)
    level = models.IntegerField()
    training = models.ForeignKey(to=Training, on_delete=models.CASCADE, related_name='training')
    enabled = models.BooleanField(default=True)
    checked = models.BooleanField(default=False)
    ata_chapter = models.ForeignKey(AtaChapter, on_delete=models.CASCADE, related_name = 'questions')
    book_page = models.CharField(max_length=20)
    issue_date = models.DateField()
    check_date = models.DateField(blank=True, null=True)
    change_date = models.DateField(blank=True, null=True)
    ref_to_old_id = models.IntegerField(default=0)
    ref_to_new_id = models.IntegerField(default=0)
    issued_by = models.CharField(max_length=30, blank=True, null=True)
    checked_by = models.CharField(max_length=30, blank=True, null=True)
    changed_by = models.CharField(max_length=30, blank=True, null=True)
    disable_reason = models.CharField(max_length=200, blank=True, null=True)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    answer = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)


class Course(models.Model):
    training = models.ForeignKey(Training, on_delete=models.CASCADE, related_name='courses')
    course_number = models.CharField(max_length=50)

class Student(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    dob = models.DateField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='students')

class Exam(models.Model):
    date = models.DateField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exams')
    ata_chapters = models.ManyToManyField(AtaChapter)
    is_reexam = models.BooleanField(default=False) # поле под вопросом
    note_for_examiner = models.CharField(max_length=50)

class ExamQuestion(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='used_in_exam')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='exam_questions')
    sequence_number = models.IntegerField()



    

