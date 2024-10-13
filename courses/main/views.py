from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .db import Users



def is_login(request):
    hash_id = request.session.get('hash_id')
    is_login = False
    
    if not(hash_id is None):
        is_login = True
    return is_login

def index(request):
    hash_id = request.session.get('hash_id')
    is_login = False
    
    if not(hash_id is None):
        is_login = True

    print(hash_id, is_login)

    return render(request, "index.html", {"is_login": is_login})

def login(request):
    if request.POST:
        users = Users()

        email = request.POST.get("email")
        password = request.POST.get("password")
        if users.is_user_in_db(email, password):
            hash_id = users.get_user_hash(email, password)
        else:
            users.insert_new_user(email, password)
            hash_id = users.get_user_hash(email, password)
        
        request.session["hash_id"] = hash_id
        response = redirect("../")
        # response.set_cookie("hash_id", hash_id, path="/")

        return response
    
    return render(request, "login.html")

def log_out(request):
    del request.session['hash_id']
    return redirect("../")

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
        
def courses(request):
    template = loader.get_template("courses.html")

    is_login = is_login(request)
    
    return HttpResponse(
        template.render(
            {"is_login": is_login
        }, request)
    )
