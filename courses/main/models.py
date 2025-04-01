from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.functions import Now
from django.core.management.base import BaseCommand
from icecream import ic
from enum import Enum

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


class SharedManager(models.Manager):
    def get_nested_lists(self, input_list, dimension):
        """
        В процессе верстки страниц курсов и курсов в профиле нам нужно распределить
        одномерный список курсов по строкам из 3-х, 4-х ячеек с этими курсами,
        данная функция получает на вход список, который нужно распределить на строки
        с элементами в количестве dimension штук
        """

        dimensions = []
        
        list_of_dimension = [None for _ in range(dimension)]
        for n, course in enumerate(input_list):
            del list_of_dimension[n % dimension]
            list_of_dimension.insert(n % dimension, course)
            if n + 1 == dimension:
                dimensions.append(list_of_dimension)
                list_of_dimension = [None for _ in range(dimension)]

        if any(list_of_dimension):
            dimensions.append(list_of_dimension)

        return dimensions


# class UserProfile(User):
#     image = models.ImageField(upload_to="profile_image", blank=True)

class Course(models.Model):
    name = models.CharField(max_length=100)
    short_desc = models.TextField(max_length=200, default="")
    desc = models.TextField(max_length=2000, default="")
    author = models.CharField(max_length=100)
    create_datetime = models.DateTimeField(default=timezone.now)
    is_visible = models.BooleanField(default=True)

    objects = SharedManager()

    @staticmethod
    def get_courses_nested_list(dimension=3):
        courses = Course.objects.filter(is_visible=True)
        return Course.objects.get_nested_lists(courses, dimension)

    @staticmethod
    def get_lessons_list(course_id):
        lessons_group = Course.objects.filter(id=course_id).first().lessons_group.all()
        lessons_list = []
        for lesson_group in lessons_group:
            for lesson in lesson_group.lesson.all():
                lessons_list.append(lesson.id)
        return lessons_list

    @staticmethod
    def get_questions_list(course_id):
        questions_group = Course.objects.filter(id=course_id).first().questions_group.all()
        questions_list = []
        for question_group in questions_group:
            for question in question_group.question.all():
                questions_list.append(question.id)
        return questions_list

class Lessons_Group(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, related_name='lessons_group', on_delete=models.CASCADE)

class Lesson(models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField()
    lesson_group = models.ForeignKey(Lessons_Group, related_name='lesson', on_delete=models.CASCADE)

class Questions_Group(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, related_name='questions_group', on_delete=models.CASCADE)

    @classmethod
    def questions_count(self, course_id) -> int:
        questions_group_obj = Questions_Group.objects.filter(
                course=Course.objects.get(id=course_id)
            ).first()
        questions_count = questions_group_obj.question.count()
        return questions_count

class Question(models.Model):
    name = models.CharField(max_length=100)
    question_condition = models.TextField()
    answers = models.JSONField()
    correct_answer = models.IntegerField(default=0)
    question_group = models.ForeignKey(Questions_Group, related_name='question', on_delete=models.CASCADE)

    @classmethod
    def get_next_question_id(self, course_id, question_id) -> int | None:
        questions_list = Course.get_questions_list(course_id)
        question_index = questions_list.index(question_id)

        if question_index + 1 >= len(questions_list):
            return None

        return questions_list[question_index + 1]

class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    is_correct = models.BooleanField()
    answer = models.IntegerField(default=-1)
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    @staticmethod
    def check_user_answer_exist(user, course, question) -> bool:
        return UserAnswer.objects.filter(
            user=user,
            course=course,
            question=question
        ).exists()

    @classmethod
    def save_user_answer(self, user_obj, course_id, question, is_correct, user_answer):
        course = Course.objects.get(id=course_id)

        return UserAnswer.objects.create(
            user=user_obj,
            course=course,
            question=question,
            is_correct=is_correct,
            answer=user_answer
        )

    @classmethod
    def get_user_answers(self, user, course_id) -> list[bool]:
        user_answers = UserAnswer.objects.filter(
            user=user, 
            course_id=Course.objects.get(
                id=course_id
            )
        ).values_list("is_correct")
        # user_answers: [(True), (False)]

        return_list = [answer_tuple[0] for answer_tuple in user_answers]
        # return_list: [True, False]

        return return_list

class ActionsCodes(Enum):
    OPEN_COURSE = 1
    OPEN_LESSON = 2
    START_TEST = 6
    OPEN_QUESTION = 3
    QUESTION_ANSWER = 4
    END_TEST = 5
    END_TEST_HIGHEST_SCORE = 7

"""
Таблица UserActions нужна, чтобы фиксировать незаконченные курсы, а также 
"""
class UserActions(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    action_code = models.IntegerField()
    user_answer = models.ForeignKey(UserAnswer, on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    is_highest_score = models.BooleanField(null=True)
    created_at = models.DateTimeField(default=timezone.now)

    objects = SharedManager()

    @classmethod
    def actions_registration(
            self,
            user, 
            action_code: ActionsCodes, 
            user_answer=None,
            course_id=None,
            lesson_id=None,
            question_id=None,
            is_highest_score=None
        ):
        # Уверен можно распаковать аргументы более элегантно, но пока оставлю так
        """
        Данная функция позволяет зарегестрировать действия пользователя из любой 
        точки кода, не прописывая каждый раз create-запрос, а просто вызвав эту 
        функцию указывая только нужные аргументы под действие 
        """
        course_obj = Course.objects.filter(id=course_id).first() if course_id != None else None
        lesson_obj = Lesson.objects.filter(id=lesson_id).first() if lesson_id != None else None
        question_obj = Question.objects.filter(id=question_id).first() if question_id != None else None
        UserActions.objects.create(
                user=user,
                action_code=action_code.value,
                user_answer=user_answer,
                course=course_obj,
                lesson=lesson_obj,
                question=question_obj,
                is_highest_score=is_highest_score
            )

    @classmethod
    def is_user_pass_test_with_highest_score(self, user_obj, course_obj) -> bool:
        """
        Единственная задача данной функции вернуть булево значение, сдавал ли 
        пользователь тест на высшую оценку когда-либо вообще?
        """
        
        user_actions = UserActions.objects.filter( 
            user=user_obj,
            course=course_obj,
            action_code=ActionsCodes.END_TEST_HIGHEST_SCORE.value
        )

        for user_action in user_actions:
            if user_action.is_highest_score == True:
                return True
        return False

    @classmethod
    def is_user_end_test(self, user_actions_list):
        is_test_started = False
        is_test_ended = False
        is_test_expired = None  # Булево значение, но вводится только для случаев, 
                                # когда тест не закончен, поэтому может быть не определен

        test_started_action_obj = None

        for action in user_actions_list:
            """
            На этом этапе я проверяю:
            * Начал ли пользователь выполнять тест?
                * Если начал, я вывожу объект действия в переменную, потому что 
                  нужно проверить когда он начал выполнять тест
            * Закончил ли пользователь выполнять тест?
            """
            match action.action_code:
                case ActionsCodes.START_TEST.value:
                    test_started_action_obj = action
                    is_test_started = True
                case ActionsCodes.END_TEST.value:
                    is_test_ended = True

        if test_started_action_obj is not None:
            action_time_without_timezone = test_started_action_obj.created_at.replace(tzinfo=None)
            print(test_started_action_obj.created_at, datetime.now() - timedelta(minutes=15))
            if action_time_without_timezone < datetime.now() - timedelta(minutes=15):
                is_test_expired = True
            else:
                is_test_expired = False

        return (is_test_started, is_test_ended, is_test_expired)

    @classmethod
    def interpretate_user_actions(self, user_obj, course_id):
        is_test_started = False
        is_test_ended = False
        is_try_fired = False
        can_continue_test = False

        course_obj = Course.objects.filter(id=course_id).first()
        todays_user_actions = UserActions.objects.filter(
            created_at__date=timezone.now().date(), 
            user=user_obj,
            course=course_obj
        ) # Получает записи, которые были сделаны сегодня

        is_user_hisghest_score_ever = UserActions.is_user_pass_test_with_highest_score(user_obj, course_obj)

        is_test_started, is_test_ended, is_test_expired = UserActions.is_user_end_test(todays_user_actions)

        if is_test_started and is_test_ended:
            is_try_fired = True
        elif is_test_started and not(is_test_ended):
            can_continue_test = True
        
        return {
            'is_test_started': is_test_started,
            'is_test_ended': is_test_ended,
            'is_user_hisghest_score_ever': is_user_hisghest_score_ever,
            'is_test_expired': is_test_expired,
            'is_try_fired': is_try_fired,
            'can_continue_test': can_continue_test
        }

    @classmethod
    def prettified_courses_list(self, courses_list):
        """
        На вход функции подается список типа: 
            [
                {'course_id': 3, 'type': 5}, 
                {'course_id': 4, 'type': 5}
            ]
        Цель данной функции добавить в словари доп инфу о курсе
        """

        for course_info in courses_list:

            courses_values = Course.objects.filter(
                id=course_info["course_id"]
            ).values_list("name", flat=True)
            
            course_info["name"] = courses_values[0]
        return courses_list
    
    @classmethod
    def get_last_question_in_unfinished_test(self, user_obj, course_id):
        course_user_actions = UserActions.objects.filter( 
            user=user_obj,
            course_id=course_id
        ).all()

        is_end_test = False
        
        actions_before_start_test = []

        for action in reversed(course_user_actions):
            if action.action_code == ActionsCodes.END_TEST.value:
                is_end_test = True
            elif action.action_code == ActionsCodes.START_TEST.value and not(is_end_test):
                break
            elif action.action_code == ActionsCodes.QUESTION_ANSWER.value:
                actions_before_start_test.append(action)
    
        print(actions_before_start_test)

        next_question_id = Question.get_next_question_id(
            course_id, 
            len(actions_before_start_test) + 1
        )
        """
        Код выше буквально говорит: я знаю, что пользователь не закончил тест 
        курса course_id, но я знаю, что он ответил на 
        len(actions_before_start_test) вопросов, какой следующий вопрос? 
        """

        result = {
            "next_question_index": len(actions_before_start_test) + 1, 
            # пользователь ответил на len(actions_before_start_test) вопросов, 
            # значит индекс следующего будет +1
            "next_question_id": next_question_id
        }

        return result
    
    @classmethod
    def get_last_try_result(self, user_obj, course_id):
        """
        Эта функция выполняется только в том случае, когда мы точно уверены, что
        пользователь завершил тест
        """

        course_user_actions = UserActions.objects.filter(
            user=user_obj,
            course_id=course_id
        ).all()
        print(course_user_actions)

        is_end_test = False
        correct_answers_count = 0
        all_answers_count = 0

        for action in reversed(course_user_actions):
            if action.action_code == ActionsCodes.END_TEST.value:
                is_end_test = True
            elif is_end_test and action.action_code == ActionsCodes.QUESTION_ANSWER.value:
                all_answers_count += 1

                if UserAnswer.objects.filter(id=action.user_answer_id).first().is_correct:
                    correct_answers_count += 1

            elif action.action_code == ActionsCodes.START_TEST.value:
                break

        return {
            "correct_answers_count": correct_answers_count,
            "all_answers_count": all_answers_count
        }

    @classmethod
    def get_user_profile_table(self, user_obj):
        """
        Суть данной фукнции в парсинге курсов, с которыми у пользователя в 
        целом есть действия.

        На странице профиля различаются 5 типов блоков:
        1) Курс завершен, тест пройден на высший балл
        2) Курс завершен, тест пройден сегодня, но не на высший балл, предлагается пересдать завтра
        3) Курс завершен, тест пройден вчера, есть активная кнопка "перейти к сдаче теста"
        4) Курс завершен, тест пройден неполностью и попытка еще не сгорела, предлагается перейти к вопросу
        5) Курс завершен, ознакомление с теорией завершено, предлагается перейти к тесту
        """

        user_courses = UserActions.objects.filter( 
            user=user_obj,
        ).values_list(
            'course', flat=True
        ).distinct()

        return_list = []

        for course_id in user_courses:
            course_info_dict = {
                "course_id": course_id
            }

            course_flags = UserActions.interpretate_user_actions(user_obj, course_id)

            is_test_started = course_flags['is_test_started']
            is_test_ended = course_flags['is_test_ended']
            is_user_hisghest_score_ever = course_flags['is_user_hisghest_score_ever']
            is_test_expired = course_flags['is_test_expired']
            is_try_fired = course_flags['is_try_fired']
            can_continue_test = course_flags['can_continue_test']

            if is_user_hisghest_score_ever:
                course_type = 1

                last_try_result = UserActions.get_last_try_result(user_obj, course_id)

                course_info_dict["last_try_info"] = last_try_result

            elif is_test_started and is_test_ended and not(is_user_hisghest_score_ever):
                if is_try_fired:
                    course_type = 2
                else:
                    course_type = 3

                last_try_result = UserActions.get_last_try_result(user_obj, course_id)

                course_info_dict["last_try_info"] = last_try_result

            elif is_test_started and not(is_test_ended) and not(is_test_expired):                
                course_type = 4

                next_question_info = UserActions.get_last_question_in_unfinished_test(user_obj, course_id)
                course_info_dict["next_question_info"] = next_question_info
            elif not(is_test_started):
                course_type = 5

            course_info_dict["type"] = course_type
            
            return_list.append(course_info_dict)

        return_list = UserActions.prettified_courses_list(return_list)

        nested_list = UserActions.objects.get_nested_lists(return_list, 3)

        print(nested_list)

        return nested_list