from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from .models import Users
import hashlib


def is_login(request):
    hash_id = request.session.get('hash_id')
    is_login = False
    
    if not(hash_id is None):
        is_login = True
    return is_login

def index(request):
    hash_id = request.session.get('hash_id')
    is_login = False
    
    print(request.user.is_authenticated)

    if not(hash_id is None):
        is_login = True

    print(hash_id, is_login)

    return render(request, "index.html", {"is_login": is_login})

def login(request):
    if request.POST:

        email = request.POST.get("email")
        password = request.POST.get("password")
        
        if Users.objects.filter(
                email=email, 
                password=password
            ).exists():
            hash_id = users.get_user_hash(email, password)
        else:
            username = "asd"
            user = Users.objects.create_user(
                email,
                password,
                hashlib.md5((email + password).encode()).hexdigest()
            )
            user.save()
            hash_id = hashlib.md5((email + password).encode()).hexdigest()

        request.session["hash_id"] = hash_id
        request.is_authenticated = True
        response = redirect("../")
        # response.set_cookie("hash_id", hash_id, path="/")

        return response
    
    return render(request, "login.html")

def log_out(request):
    del request.session['hash_id']
    return redirect("../")

@login_required
def profile(request):
    is_login = is_login(request)
    
    if is_login:
        template = loader.get_template("profile.html")
        context = {
            "is_login": is_login,
        }
        return HttpResponse(
            template.render(
                {"is_login": is_login
            }, request)
        )
    else:
        return redirect("/login")
        
def courses_overview(request):
    template = loader.get_template("courses.html")

    is_login = is_login(request)
    
    return HttpResponse(
        template.render(
            {"is_login": is_login
        }, request)
    )

def course_page(request):
    template = loader.get_template("courses.html")

    is_login = is_login(request)
    
    return HttpResponse(
        template.render(
            {"is_login": is_login
        }, request)
    )