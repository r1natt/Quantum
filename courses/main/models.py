from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.functions import Now

"""
От бд нужно:
хранить пользователей
хранить курсы, теорию, тесты

Каждый пользователь может проходить несколько курсов
Каждый курс имеет несколько записей о теории и тестах


Таблицы:
users
courses
lessons
    lesson
questions
    question у каждого вопроса есть id курса, id вопроса 
"""


class Course(models.Model):
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=1000, default="")
    author = models.CharField(max_length=100)
    create_datetime = models.DateTimeField(default=timezone.now)

class Lessons_Group(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, related_name='lessons_group', on_delete=models.CASCADE)

class Lesson(models.Model):
    name = models.CharField(max_length=100)
    content = models.CharField(max_length=10000)
    lesson_group = models.ForeignKey(Lessons_Group, related_name='lesson', on_delete=models.CASCADE)

class Questions_Group(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, related_name='questions_group', on_delete=models.CASCADE)

class Question(models.Model):
    name = models.CharField(max_length=100)
    question_condition = models.CharField(max_length=10000)
    answers = models.JSONField()
    correct_answer = models.IntegerField(default=0)
    question_group = models.ForeignKey(Questions_Group, related_name='question', on_delete=models.CASCADE)

class UserAnswer(models.Model):
    user = models.ForeignKey(User, related_name='user_choices', on_delete=models.DO_NOTHING)
    is_correct = models.BooleanField()
    user_answer = models.IntegerField(default=-1)
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, default=-1)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
