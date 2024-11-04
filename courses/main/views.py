from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import (
    User, 
    Course,
    Lesson, 
    LessonModule,
    QuestionModule,
    Question,
    UserAnswer
)
from .forms import RegisterForm

from .course_structure import course_data


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

def courses_overview(request):
    return render(request, 'courses.html', {"user": request.user})

def course_page(request, course_id):
    return render(request, 'course_page.html', {
            "user": request.user, 
            "course_data": course_data, 
            "name": course_data.name
        }
    )

def lesson_page(request, course_id, lesson_id):
    # lesson_data = Lesson.objects.filter(LessonModule.objects.filter(course_id=course_id).values('id')=lesson_id)
    # lesson_data = Lesson.objects.filter().values('id')
    # lesson_data = Lesson.objects.select_related('lessons_module')
    lesson_data = list(Lesson.objects.values("id"))
    print(lesson_data)
    return render(request, 'lesson_page.html', {"user": request.user})

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

def test_page(request, course_id, question_id):
    if request.method == "POST":
        answer = request.POST.get("answer")
        print(answer)

    return render(
        request, 
        'test_page.html', 
        {
            "user": request.user, 
            "course_name": course_data.name,
            "question": get_question(course_id, question_id)
        }
    )


    