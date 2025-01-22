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
    # ActionType,
    # Action
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

@login_required
def courses_overview(request):
    return render(request, 'courses.html', {"user": request.user})

@login_required
def course_page(request, course_id):

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

@login_required
def lesson_page(request, course_id, lesson_id):
    lesson_data = Lesson.objects.filter(id=lesson_id).first()

    lessons_list = get_lessons_list(course_id)
    questions_group = get_questions_list(course_id)
    
    lesson_index = lessons_list.index(lesson_id)
    ic(lesson_index)
    ic(lessons_list)
    ic(lesson_index == len(lessons_list) - 1)

    if lesson_index == 0:
        prev = f'/courses/{course_id}'
    else:
        prev = f'/courses/{course_id}/lesson/{lessons_list[lesson_index - 1]}'

    
    if lesson_index == len(lessons_list) - 1:
        next = f'/courses/{course_id}/test/{questions_group[0]}'
    else:
        next = f'/courses/{course_id}/lesson/{lessons_list[lesson_index + 1]}'

    return render(
        request, 
        'lesson_page.html', 
        {
            "user": request.user,
            "lesson_data": lesson_data,
            "prev": prev,
            "next": next
        }
    )

def get_question(course_id, question_id):
    chapters = course_data.chapters

    for chapter in chapters:
        if chapter.type == 2:
            questions = chapter.questions
            break

    for question in questions:
        if question.order == question_id:
            return question
    return -1

def get_user_answer(request_obj, answers) -> int:
    return int(request_obj.POST['answer'])

def save_user_answer(user_obj, course_id, question, is_correct, user_answer):
    UserAnswer.objects.create(
        user=user_obj,
        course=Course.objects.get(id=course_id),
        question=question,
        is_correct=is_correct,
        answer=user_answer
    )

@login_required
def question_page(request, course_id, question_id):

    questions_list = get_questions_list(course_id)
    question_index = questions_list.index(question_id)

    question_obj = Question.objects.filter(id=question_id).first()
    answers = question_obj.answers 

    question = get_question(course_id, question_id)

    if request.method == "POST":
        user_answer = get_user_answer(request, answers)
        is_correct = False

        ic(type(user_answer))
        ic(user_answer)
        ic(question.correct_answer)

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
            question_obj,
            is_correct,
            user_answer
        )

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
            "question": question_obj
        }
    )

def test_page(request):
    course_query = Course.objects.filter(id=1)[0]
    ic(course_query.id)
    ic(dir(course_query))
    ic(course_query.lessons_group.all())
    course_id = course_query.id
    
    lessons_groups = Lessons_Group.objects.filter(course=course_id)
    ic(lessons_groups)

    for lesson_group in lessons_groups:
        lessons = Lesson.objects.filter(lesson_group=lesson_group.id)
        for lesson in lessons:
            ic(lesson.content)
    return HttpResponse("Hello!")
