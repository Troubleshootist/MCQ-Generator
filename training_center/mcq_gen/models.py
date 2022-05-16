from django.db import models


class BaseModel(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True


class Training(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class AtaChapter(BaseModel):
    ata_digit = models.CharField(max_length=10)
    ata_description = models.CharField(max_length=300)

    def __str__(self):
        return self.ata_digit


class Requirements(BaseModel):
    training = models.ForeignKey(
        Training, on_delete=models.CASCADE, related_name='requirements')
    ata = models.ForeignKey(
        AtaChapter, on_delete=models.CASCADE, related_name='requirements')
    questions_number = models.IntegerField()
    level = models.IntegerField()

    def __str__(self):
        return f'Training: {self.training.name}, ATA: {self.ata.ata_digit}'


class Question(BaseModel):
    question = models.CharField(max_length=400)
    level = models.IntegerField(default=100)
    training = models.ForeignKey(
        to=Training, on_delete=models.CASCADE, related_name='training')
    enabled = models.BooleanField(default=True)
    checked = models.BooleanField(default=False)
    ata_chapter = models.ForeignKey(
        AtaChapter, on_delete=models.CASCADE, related_name='questions')
    book_page = models.CharField(max_length=100)
    issue_date = models.DateField(null=True)
    check_date = models.DateField(blank=True, null=True)
    change_date = models.DateField(blank=True, null=True)
    ref_to_old_id = models.IntegerField(default=0)
    ref_to_new_id = models.IntegerField(default=0)
    issued_by = models.CharField(max_length=100, blank=True, null=True)
    checked_by = models.CharField(max_length=100, blank=True, null=True)
    changed_by = models.CharField(max_length=100, blank=True, null=True)
    disable_reason = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.question


class Answer(BaseModel):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='answers')
    answer = models.CharField(max_length=400, default=False)
    correct = models.BooleanField(default=False)


class Course(BaseModel):
    training = models.ForeignKey(
        Training, on_delete=models.CASCADE, related_name='courses')
    course_number = models.CharField(max_length=50)

    def __str__(self):
        return " ,".join((self.course_number, self.training.name))


class Student(BaseModel):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    dob = models.DateField()
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='students')

    def __str__(self):
        return " ,".join((self.surname, self.course.course_number, self.course.training.name))


class Exam(BaseModel):
    date = models.DateField()
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='exams')
    ata_chapters = models.ManyToManyField(AtaChapter)
    questions = models.ManyToManyField(Question)
    note_for_examiner = models.CharField(max_length=50)


class QuestionSequence(BaseModel):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='sequences')
    exam = models.ForeignKey(
        Exam, on_delete=models.CASCADE, related_name='sequences')
    sequence_number = models.IntegerField(verbose_name='Seq. number')


class QuestionResult(BaseModel):
    exam = models.ForeignKey(
        Exam, on_delete=models.CASCADE, related_name='results', default=None)
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='results', default=None)
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='results', default=None)
    is_correct = models.BooleanField(default=False)
