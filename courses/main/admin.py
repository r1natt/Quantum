from django.contrib import admin
from .models import Course, LessonModule, Lesson, QuestionModule, Question, UserAnswer


# Register your models here.
admin.site.register(Course)
admin.site.register(LessonModule)
admin.site.register(Lesson)
admin.site.register(QuestionModule)
admin.site.register(Question)
admin.site.register(UserAnswer)