from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("user/", views.user, name="user"),
    path("courses/", views.courses, name="courses"),
]
