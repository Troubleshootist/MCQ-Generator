from django.contrib import admin
from . import models

admin.site.register(models.Question)
admin.site.register(models.Answer)
admin.site.register(models.Course)
admin.site.register(models.Student)
admin.site.register(models.Training)
admin.site.register(models.AtaChapter)
admin.site.register(models.Exam)
admin.site.register(models.ExamQuestion)