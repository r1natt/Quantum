from icecream import ic

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import (
    User, 
    Course,
    Lessons_Group,
    Lesson,
    Questions_Group,
    Question,
    UserAnswer
)
from .forms import RegisterForm

from .course_structure import course_data

from django.http import HttpResponse


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

def get_user_answer(request_obj):
    answers = [
        request_obj.POST.get("answer1"),
        request_obj.POST.get("answer2"),
        request_obj.POST.get("answer3"),
        request_obj.POST.get("answer4")
    ]

    for n, answer in enumerate(answers):
        if answer:
            return str(n + 1)
            # возвращаю строку потому что буду сравнивать это значение дальше со строкой 

def save_user_answer(user_id, course_id, question_id, is_correct, user_answer):
    UserAnswer.objects.create(
        user=user_id,
        course=course_id,
        question=question_id,
        is_correct=is_correct,
        user_answer=user_answer
    )

@login_required
def question_page(request, course_id, question_id):

    question = get_question(course_id, question_id)

    if request.method == "POST":
        user_answer = get_user_answer(request)
        is_correct = False

        if user_answer == question.correct_answer:
            is_correct = True
            print(f'{question_id} correct answer! ({user_answer})')
        else:
            print(f'{question_id} incorrect_answer :( ({user_answer})')
        
        save_user_answer(
            request.user.id,
            course_id,
            question_id,
            is_correct,
            user_answer
        )
        
        if get_question(course_id, question_id + 1) == -1:
            # Проверяю есть ли следующий вопрос и если его нет, то направляю на страницу результатов
            return redirect('/tests/results')
        else:
            return redirect(f'/tests/{course_id}/{question_id + 1}')

    return render(
        request, 
        'test_page.html', 
        {
            "user": request.user, 
            "course_name": course_data.name,
            "question": question
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