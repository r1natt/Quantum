from django.db import models
from datetime import datetime
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

# class UserProfile(User):
#     image = models.ImageField(upload_to="profile_image", blank=True)

class Course(models.Model):
    name = models.CharField(max_length=100)
    short_desc = models.CharField(max_length=200, default="")
    desc = models.CharField(max_length=2000, default="")
    author = models.CharField(max_length=100)
    create_datetime = models.DateTimeField(default=timezone.now)

    @staticmethod
    def get_nested_lists(input_list, dimension):
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

    @staticmethod
    def get_courses_nested_list(dimension=3):
        courses = Course.objects.all()
        return Course.get_nested_lists(courses, dimension)

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
    
    @staticmethod
    def unparse_imgs(text):
        """
        Довольно костыльная функция, для которой еще и контекст нужен

        Контекст: лекции состоят не только из текста, но и картинок. 
        Эти картинки должны быть как-то выведены посередине текста. 
        Чтобы этого добиться я ввожу тэги <img>img_name.png<\img> непосредственно 
        в самом тексте (это значит, что эту конструкцию я буду хранить в бдшке и не 
        смогу проверять ошибки тэгов при создании новой лекции).
        
        Это плохо, но вводить парсинг полноценного markdown с проверками 
        корректности markdown в таком маленьком проекте только ради картинок я 
        считаю избыточным)

        Еще это плохо потому что я начинаю в бдшке хранить почти уже html, но еще 
        не html, но он почти уже html
        """
        pattern = r'\<\s*img\s*\>(.*?)\<\\s*img\s*\>' # regex паттерн: <img>file_name.png<\img> -> file_name.png
        text = re.sub(pattern, r'<img id="ikbxfs" src="/main/static/images/lessons/\1" />', text)
        """
        В строке выше костыли продолжаются

        Теперь я знаю имена файлов картинок, которые нужно вставить посреди текста, 
        но у картинок уже есть свои стили, и это проблема, потому что я хардкожу имя 
        css на уровне бэкенда, и если я изменю id стиля картинки, я даже не пойму, 
        почему картинка не форматируется как я хочу.
        
        Я понимаю это и принимаю этот риск🙏 (я устал и мне смешно)

        Есть другое решение, заместо замены моих тэгов html тэгами (как это происходит сейчас), в таблицу 
        lesson добавить столбец imgs_list (JSON type) и туда через запятую записать 
        имена картинок, а в тексте записать индексы этих картинок, где они должны 
        быть вставлены, вот так:
        
        a = '''something text 
        img_1
        img_2
        asdasd'''

        Но это еще хуже, если я ошибусь, и добавлю лишний индекс:
        a = '''something text 
        img_1
        img_2
        img_3
        asdasd'''
        То нет правильного решения в этой проблеме:
        1) Если я проигнорирую этот индекс, может быть такое, что я в список забыл 
        внести картинку, и тогда просто потеряю ее на фронте
        2) Если я выведу это как ошибку, то каждый раз мне придется смотреть решение
        ошибки в бдшке, что тоже не предел мечтаний

        Как итог получается что я лучше нарушу правило хранение в бдшке только 
        текста и буду хранить тэги тоже, чем бесконечно копаться в ошибках  
        """
        return text

    @staticmethod
    def unparse_lesson_text(text):
        # TODO выделить text в класс как объект, чтобы применять функции анпарса в внутри класса, который наследуется от text
        text = text.replace('\n', '<br>')
        text = Lesson.unparse_imgs(text)
        return text

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
    question_condition = models.CharField(max_length=10000)
    answers = models.JSONField()
    correct_answer = models.IntegerField(default=0)
    question_group = models.ForeignKey(Questions_Group, related_name='question', on_delete=models.CASCADE)

class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    is_correct = models.BooleanField()
    answer = models.IntegerField(default=-1)
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

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
        
        is_in_db = UserAnswer.check_user_answer_exist(user_obj, course, question)
        if not is_in_db:
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
    OPEN_COURSE = 1#
    OPEN_LESSON = 2 # 
    START_TEST = 6 # 
    OPEN_QUESTION = 3 # 
    QUESTION_ANSWER = 4 # 
    END_TEST = 5

"""
Таблица UserActions нужна, чтобы фиксировать незаконченные курсы, а также 
"""
class UserActions(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    action_code = models.IntegerField()
    user_answer = models.ForeignKey(UserAnswer, on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.DO_NOTHING, null=True)
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING, null=True)

    @classmethod
    def actions_registration(
            self,
            user, 
            action_code: ActionsCodes, 
            user_answer=None,
            course_id=None,
            lesson_id=None,
            question_id=None
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
                question=question_obj
            )