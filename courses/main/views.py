from icecream import ic

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from enum import Enum
import re
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
from django.http import HttpResponse, JsonResponse


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

def calc_view(request):
    return render(request, 'calc.html')

@login_required
def profile(request):

    user_actions_list = UserActions.get_user_profile_table(request.user)

    return render(
        request, 
        'profile.html', 
        {
            "user": request.user,
            "nested_list": user_actions_list
        }
    )

@login_required
def courses_overview(request):
    courses = Course.get_courses_nested_list()
    return render(
        request, 
        'courses.html', 
        {
            "user": request.user,
            "courses_nested_list": courses
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
    UserActions.actions_registration(
        request.user, 
        ActionsCodes.OPEN_COURSE,
        course_id=course_id
    )
    return render(request, 'course_page.html', {
            "user": request.user, 
            "course_data": Course.objects.filter(id=course_id).first()
        }
    )

@login_required
def lesson_page(request, course_id, lesson_id):
    lesson_data = Lesson.objects.filter(id=lesson_id).first()

    lessons_list = Course.get_lessons_list(course_id)
    questions_group = Course.get_questions_list(course_id)
    
    lesson_index = lessons_list.index(lesson_id)

    UserActions.actions_registration(
        request.user,
        ActionsCodes.OPEN_LESSON,
        course_id=course_id,
        lesson_id=lesson_id
    )

    if lesson_index == 0:
        prev = f'/courses/{course_id}'
    else:
        prev = f'/courses/{course_id}/lesson/{lessons_list[lesson_index - 1]}'

    if lesson_index == len(lessons_list) - 1:
        next = f'/courses/{course_id}/test/intro'
    else:
        next = f'/courses/{course_id}/lesson/{lessons_list[lesson_index + 1]}'

    text = lesson_data.content

    return render(
        request,    
        'lesson_page.html', 
        {
            "user": request.user,
            "lesson_data": {
                "name": lesson_data.name,
                "text": text
            },
            "prev": prev,
            "next": next
        }
    )

@login_required
def test_intro(request, course_id):
    user_acts = UserActions.interpretate_user_actions(request.user, course_id)
    print(user_acts)
    if user_acts["is_try_fired"]:
        return render(
            request, 
            'tries_is_over.html', 
            {
                "user": request.user
            }
        )
    else:
        return render(
            request, 
            'test_intro.html', 
            {
                "user": request.user,
                "first_question_id": Course.objects.filter(
                    id=course_id
                    ).first().questions_group.first().id
            }
        )

def get_user_answer(request_obj) -> int | None:
    return int(request_obj.POST['answer']) if 'answer' in request_obj.POST.keys() else None

@login_required
def question_page(request, course_id, question_id):

    question = Question.objects.filter(id=question_id).first()
    answers = question.answers

    questions_list = Course.get_questions_list(course_id)
    question_index = questions_list.index(question_id)

    if question_index == 0:
        UserActions.actions_registration(
            request.user,
            ActionsCodes.START_TEST,
            course_id=course_id
        )

    # question = get_question(course_id, question_id)

    if request.method == "POST":
        user_answer = get_user_answer(request)
        is_correct = False

        if user_answer is None:
            return redirect(f"/courses/{course_id}/test/{question_id}")

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
        
        answer_obj = UserAnswer.save_user_answer(
            request.user,
            course_id,
            question,
            is_correct,
            user_answer
        )

        UserActions.actions_registration(
            request.user,
            ActionsCodes.QUESTION_ANSWER,
            course_id=course_id,
            question_id=question_id,
            user_answer=answer_obj
        )
        
        next_question_id = Question.get_next_question_id(course_id, question_id)
        
        if next_question_id is None:
            # Проверяю есть ли следующий вопрос и если его нет, то направляю на страницу результатов
            redirect_page = f'/courses/{course_id}/test/results'
        else:
            redirect_page = f'/courses/{course_id}/test/{next_question_id}'
        return redirect(redirect_page)

    UserActions.actions_registration(
        request.user,
        ActionsCodes.OPEN_QUESTION,
        course_id=course_id,
        question_id=question_id
    )

    return render(
        request, 
        'test_page.html', 
        {
            "user": request.user, 
            "course_name": course_data.name,
            "question": question
        }
    )

@login_required
def test_results_page(request, course_id):
    
    UserActions.actions_registration(
        request.user,
        ActionsCodes.END_TEST,
        course_id=course_id
    )

    this_try_result = UserActions.get_last_try_result(request.user, course_id)

    print(this_try_result)

    answer_percent = this_try_result["correct_answers_count"] / this_try_result["all_answers_count"]

    if answer_percent <= 0.4:
        text = "Вам бы лучше пересдать тестик завтра..."
    elif answer_percent <= 0.7:
        text = "Есть куда расти"
    else:
        text = "Чудесный результат!"

        """
        Ниже приведен костыль, на этом костыле все и держиться. 
        
        Дело в том, что если пользователь хоть раз сдал тест на высший балл, 
        на странице прогресса я должен фиксировать высший балл всегда.

        При сборке страницы с прогрессом я всегда определяю сдал ли пользователь 
        хоть раз тест на высший балл или нет. Проблема создается на моменте 
        подсчета ответов в нынешнем тесте. Чтобы подсчитать правильные ответы я 
        сначала определяю какое событие имеет код завершения теста, значит далее
        идут события ответа на вопросы и я их паршу до момента события начала 
        теста. 
        
        Проблема в том, что событие конца теста, уже должно содержать инфу о том, 
        сдал ли пользователь на высший балл или нет. Поэтому я сначала делаю 
        событие окончания теста в этой же функции в самом начале и уже потом, 
        если пользователь сдал на высший балл, я создаю идентичное событие, но 
        с указанием, что данный тест завершен на высший балл.

        UPDATE: Теперь вся эта логика происходит не просто со статусом END_TEST, 
        а END_TEST_HIGHEST_SCORE, тем самым логически разделяя эти статусы.
        """

        UserActions.actions_registration(
            request.user,
            ActionsCodes.END_TEST_HIGHEST_SCORE,
            course_id=course_id, 
            is_highest_score=True
        )

    return render(
        request, 
        'results.html', 
        {
            "user": request.user, 
            "course_obj": Course.objects.get(id=course_id),
            "question_group": Questions_Group.objects.filter(
                course=Course.objects.get(id=course_id)
            ).first(),
            "results": this_try_result,
            "text": text
        }
    )

def test_page(request):
    # ans = UserActions.interpretate_user_actions(request.user, 3)
    # print(ans)

    return render(
        request, 
        "test.html",
        {
            "text": text
        }
    )
