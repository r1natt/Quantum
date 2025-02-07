from icecream import ic

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from enum import Enum
from .models import (
    User, 
    Course,
    Lessons_Group,
    Lesson,
    Questions_Group,
    Question,
    UserAnswer,
    UserActions,

    ActionsCodes
)

from .forms import RegisterForm
from .course_structure import course_data
from django.http import HttpResponse
# from .action_types import (
#     ActionTypeEnum,
#     get_action_type_obj
# )


def index(request):
    return render(request, "index.html", {"user": request.user})

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form':form})

def login_view(request):
    error_message = None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next') or 'index'
            return redirect(next_url)
        else:
            error_message = "Invalid credentials"
    return render(request, 'login.html', {'error': error_message})

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def profile(request):
    return render(request, 'profile.html', {"user": request.user})

def actions_registration(
        user, 
        action_code: ActionsCodes, 
        user_answer=None,
        course_id=None,
        lesson_id=None,
        question_group_id=None
    ):
    # Уверен можно распаковать аргументы более элегантно, но пока оставлю так
    """
    Данная функция позволяет зарегестрировать действия пользователя из любой 
    точки кода, не прописывая каждый раз create-запрос, а просто вызвав эту 
    функцию указывая только нужные аргументы под действие 
    """
    UserActions.objects.create(
            user=user,
            action_code=action_code.value,
            user_answer=user_answer,
            course=course_id,
            lesson=lesson_id,
            question_group=question_group_id
        )
    

def get_nested_lists(input_list, dim):
    """
    В процессе верстки страниц курсов и курсов в профиле нам нужно распределить
    одномерный список курсов по строкам из 3-х, 4-х ячеек с этими курсами,
    данная функция получает на вход список, который нужно распределить на строки
    с элементами в количестве dim штук
    
    Примеры:
    Вход: 
        input_list = [1, 2, 3, 4, 5, 6] 
        n = 5
    Выход:
        [[1, 2, 3, 4, 5], [6, None, None, None, None]]

    Вход: 
        input_list = [1, 2, 3, 4, 5, 6] 
        n = 3
    Выход:
        [[1, 2, 3], [4, 5, 6]]

    Вход: 
        input_list = [1, 2, 3] 
        n = 3
    Выход:
        [[1, 2, 3]]

    """

    dims = []
    
    list_of_dim = [None for _ in range(dim)]
    for n, course in enumerate(input_list):
        del list_of_dim[n % dim]
        list_of_dim.insert(n % dim, course)
        if n + 1 == dim:
            dims.append(list_of_dim)
            list_of_dim = [None for _ in range(dim)]

    if any(list_of_dim):
        dims.append(list_of_dim)

    return dims

@login_required
def courses_overview(request):
    courses = Course.objects.all()
    nested_lists = get_nested_lists(courses, 3)
    print(nested_lists)
    return render(
        request, 
        'courses.html', 
        {
            "user": request.user,
            "courses_nested_list": nested_lists
        }
    )

@login_required
def course_intro(request, course_id):
    return render(request, 'course_intro.html', {
            "user": request.user, 
            "course_data": Course.objects.filter(id=course_id).first(),
            "next": f"/courses/{course_id}/structure"
        }
    )

@login_required
def course_page(request, course_id):
    actions_registration(request.user, ActionsCodes.OPEN_COURSE)
    return render(request, 'course_page.html', {
            "user": request.user, 
            "course_data": Course.objects.filter(id=course_id).first()
        }
    )

def get_lessons_list(course_id):
    lessons_group = Course.objects.filter(id=course_id).first().lessons_group.all()
    lessons_list = []
    for lesson_group in lessons_group:
        for lesson in lesson_group.lesson.all():
            lessons_list.append(lesson.id)
    return lessons_list

def get_questions_list(course_id):
    questions_group = Course.objects.filter(id=course_id).first().questions_group.all()
    questions_list = []
    for question_group in questions_group:
        for question in question_group.question.all():
            questions_list.append(question.id)
    return questions_list

def parse_lesson_text(text) -> str:
    pass

@login_required
def lesson_page(request, course_id, lesson_id):
    lesson_data = Lesson.objects.filter(id=lesson_id).first()

    lessons_list = get_lessons_list(course_id)
    questions_group = get_questions_list(course_id)
    
    lesson_index = lessons_list.index(lesson_id)

    if lesson_index == 0:
        prev = f'/courses/{course_id}'
    else:
        prev = f'/courses/{course_id}/lesson/{lessons_list[lesson_index - 1]}'

    
    if lesson_index == len(lessons_list) - 1:
        next = f'/courses/{course_id}/test/{questions_group[0]}'
    else:
        next = f'/courses/{course_id}/lesson/{lessons_list[lesson_index + 1]}'

    imgs = ["first.gif", "second.gif"]

    return render(
        request, 
        'lesson_page.html', 
        {
            "user": request.user,
            "lesson_data": lesson_data,
            "imgs": imgs,
            "prev": prev,
            "next": next
        }
    )

# def get_question(course_id, question_id):
#     chapters = course_data.chapters

#     for chapter in chapters:
#         if chapter.type == 2:
#             questions = chapter.questions
#             break

#     for question in questions:
#         if question.order == question_id:
#             return question
#     return -1

def get_user_answer(request_obj) -> int:
    return int(request_obj.POST['answer'])

def check_user_answer_exist(user, course, question) -> bool:
    return UserAnswer.objects.filter(
        user=user,
        course=course,
        question=question
    ).exists()

def save_user_answer(user_obj, course_id, question, is_correct, user_answer):
    course = Course.objects.get(id=course_id)
    
    is_in_db = check_user_answer_exist(user_obj, course, question)
    if not is_in_db:
        UserAnswer.objects.create(
            user=user_obj,
            course=course,
            question=question,
            is_correct=is_correct,
            answer=user_answer
        )

@login_required
def question_page(request, course_id, question_id):

    question = Question.objects.filter(id=question_id).first()
    answers = question.answers 

    # question = get_question(course_id, question_id)

    if request.method == "POST":
        user_answer = get_user_answer(request)
        is_correct = False

        if user_answer == int(question.correct_answer):
            """
            int(question.correct_answer) - я дополнительно делаю ответ числом, 
            потому что question.correct_answer выдается строкой, хотя в модельке
            прописано что поле correct_answer число, хз где все идет не так
            """
            is_correct = True
            print(f'question_id: {question_id} - correct answer! ({user_answer})')
        else:
            print(f'{question_id} incorrect_answer :( ({user_answer})')
        
        save_user_answer(
            request.user,
            course_id,
            question,
            is_correct,
            user_answer
        )
        
        questions_list = get_questions_list(course_id)
        question_index = questions_list.index(question_id)
        
        if question_index == len(questions_list) - 1:
            # Проверяю есть ли следующий вопрос и если его нет, то направляю на страницу результатов
            redirect_page = f'/courses/{course_id}/test/results'
        else:
            redirect_page = f'/courses/{course_id}/test/{questions_list[question_index + 1]}'
        return redirect(redirect_page)

    return render(
        request, 
        'test_page.html', 
        {
            "user": request.user, 
            "course_name": course_data.name,
            "question": question
        }
    )

def get_user_answers(user, course_id) -> list[bool]:
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

def questions_count(course_id) -> int:
    questions_group_obj = Questions_Group.objects.filter(
            course=Course.objects.get(id=course_id)
        ).first()
    questions_count = questions_group_obj.question.count()
    return questions_count

@login_required
def test_results_page(request, course_id):
    user_answers = get_user_answers(request.user, course_id=course_id)
    questions_c = questions_count(course_id)

    answer_percent = sum(user_answers) / questions_c

    if answer_percent <= 0.4:
        text = "Вам бы лучше пересдать тестик завтра..."
    elif answer_percent <= 0.7:
        text = "Есть куда расти"
    else:
        text = "Чудесный результат!"

    if len(user_answers) == questions_c:
        return render(
            request, 
            'results.html', 
            {
                "user": request.user, 
                "course_obj": Course.objects.get(id=course_id),
                "question_group": Questions_Group.objects.filter(
                    course=Course.objects.get(id=course_id)
                ).first(),
                "correct_answers": sum(user_answers),
                "questions_count": questions_c,
                "text": text
            }
        )
    else:
        HttpResponse("Сделать обработку ошибки, если количество ответов не равно количеству вопросов в тесте")
    


def test_page(request):
    course_operations = DBOperations(Course)
    print(course_operations.filter_by_id(id=1))

    return HttpResponse("Hello!")
