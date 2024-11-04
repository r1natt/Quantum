from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.utils import timezone

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
    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=250)
    author = models.CharField(max_length=50)

class LessonModule(models.Model):
    name = models.CharField(max_length=50)

class Lesson(models.Model):
    lesson_text = models.CharField(max_length=1000)
    lesson_module = models.ForeignKey(LessonModule, related_name='lesson', on_delete=models.CASCADE)

class QuestionModule(models.Model):
    name = models.CharField(max_length=50)

class Question(models.Model):
    question_text = models.CharField(max_length=1000)
    question_module = models.ForeignKey(QuestionModule, related_name='question', on_delete=models.CASCADE)

class UserAnswer(models.Model):
    user = models.ForeignKey(User, related_name='user_choices', on_delete=models.DO_NOTHING)
    is_correct = models.BooleanField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)


# class Questions(models.Model):
#     question_text = models.CharField(max_length=200)
#     pub_date = models.DateTimeField("date published")


# class Choice(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)