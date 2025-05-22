from django.contrib import admin
from .models import (
    Course, 
    Lessons_Group, 
    Lesson, 
    Questions_Group, 
    Question, 
    UserAnswer,
    UserActions,
    TaskGroup,
    Task
)

admin.site.register(Course)
admin.site.register(Lessons_Group)
admin.site.register(Lesson)
admin.site.register(Questions_Group)
admin.site.register(Question)
admin.site.register(UserAnswer)
admin.site.register(UserActions)
admin.site.register(TaskGroup)
admin.site.register(Task)