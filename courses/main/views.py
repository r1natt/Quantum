from django.shortcuts import render, redirect
from django.http import HttpResponse
from .db import Users


def index(request):
    return render(request, "./index.html")

def login(request):
    if request.POST:
        users = Users()

        email = request.POST.get("email", "Undefined")
        password = request.POST.get("password")
        if users.is_user_in_db(email, password):
            hash_id = users.get_user_hash(email, password)
        else:
            users.insert_new_user(email, password)
            hash_id = users.get_user_hash(email, password)
        
        response = redirect("./index.html")
        response.set_cookie("hash_id", hash_id)

        return response
    
    return render(request, "./login.html")

def user(request):
    return HttpResponse("This is user page")

def courses(request):
    return HttpResponse("This is page with courses")
