from pydantic import BaseModel, PositiveInt
from datetime import datetime

class Question(BaseModel):
    order: PositiveInt
    question: str
    answers: list[str]
    correct_answer: str

class Lesson(BaseModel):
    order: PositiveInt
    name: str
    text: str

class Chapter(BaseModel):
    type: PositiveInt
    order: PositiveInt
    name: str

class TestChapter(Chapter):
    questions: list[Question]

class TheoryChapter(Chapter):
    lessons: list[Lesson]

class Course(BaseModel):
    id: PositiveInt
    name: str
    author: str
    create_datetime: datetime
    chapters: list[TheoryChapter | TestChapter]


course = {
    "id": 1,
    "name": "Коаксиальные кабели",
    "author": "Стасян",
    "create_datetime": datetime.now(),
    "chapters": [
        {
            "type": 1, # Глава с теорией
            "order": 1, # Order - порядок отображения глав на сайте 
            "name": "Первая глава",
            "lessons" : [
                {
                    "order": 1,
                    "name": "Название урока 1",
                    "text": "Какая то теория по уроку"
                },
                {
                    "order": 2,
                    "name": "Название урока 2",
                    "text": "Какая то теория по уроку"
                },
                {
                    "order": 3,
                    "name": "Название урока 3",
                    "text": "Какая то теория по уроку"
                },
            ]
        },
        {
            "type": 1, # Глава с теорией
            "order": 2, # Order - порядок отображения глав на сайте 
            "name": "Вторая глава",
            "lessons" : [
                {
                    "order": 1,
                    "name": "Название урока 1",
                    "text": "Какая то теория по уроку"
                },
                {
                    "order": 2,
                    "name": "Название урока 2",
                    "text": "Какая то теория по уроку"
                }
            ]
        },
        {
            "type": 2, # Тест
            "order": 2,
            "name": "Тест",
            "questions" : [
                {
                    "order": 1,
                    "question": "Какой диапазон частот используется для коаксиальных кабелей?",
                    "answers": [
                        "От 60 кГц до 1 ГГц", 
                        "От 60 кГц до 10 ГГц", 
                        "От 60 кГц до 100 ГГц", 
                        "От 60 кГц до 100 МГц"],
                    "correct_answer": "2"
                },
                {
                    "order": 2,
                    "question": "Какие параметры используются для расчёта вторичных параметров передачи коаксиальных кабелей?",
                    "answers": [
                        "Габаритные размеры (d и D) и параметры изоляции (ε и tg δ)", 
                        "Длина кабеля и сопротивление материала",
                        "Диаметр внутреннего проводника и ёмкость", 
                        "Все вышеперечисленное"],
                    "correct_answer": "2"
                },
                {
                    "order": 3,
                    "question": "Как рассчитывается коэффициент затухания а для коаксиальных кабелей?",
                    "answers": [
                        "Через активные сопротивления проводников", 
                        "Через проводимости металлов",
                        "Через геометрические параметры кабеля", 
                        "Через все вышеперечисленные параметры"],
                    "correct_answer": "2"
                },
                {
                    "order": 4,
                    "question": "Как влияет замена медных проводников на алюминиевые на затухание коаксиального кабеля?",
                    "answers": [
                        "Затухание не изменяется",
                        "Затухание увеличивается на 29%",
                        "Затухание уменьшается на 29%", 
                        "Затухание зависит от соотношения радиусов проводников"],
                    "correct_answer": "2"
                },
                {
                    "order": 5,
                    "question": "Как влияет соотношение радиусов проводников rb/ra на затухание коаксиального кабеля?",
                    "answers": [
                        "Затухание не изменяется", 
                        "Затухание увеличивается",
                        "Затухание уменьшается", 
                        "Затухание зависит от геометрических параметров кабеля"],
                    "correct_answer": "2"
                },
                {
                    "order": 6,
                    "question": "Какие материалы используются для изготовления проводников коаксиальных кабелей?",
                    "answers": [
                        "Медь и алюминий",
                        "Серебро и золото",
                        "Вольфрам и молибден", 
                        "Все вышеперечисленные материалы"],
                    "correct_answer": ""
                },
                {
                    "order": 7,
                    "question": "Какие факторы влияют на выбор материала для проводников коаксиальных кабелей?",
                    "answers": [
                        "Стоимость, электрические свойства и механическая прочность",
                        "Только электрические свойства",
                        "Только стоимость и механическая прочность", 
                        "Все вышеперечисленные факторы"],
                    "correct_answer": ""
                },
            ]
        }
    ]
}

course_data = Course(**course)