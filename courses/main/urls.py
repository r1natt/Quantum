from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("log_out/", views.log_out, name="login"),
    path("profile/", views.profile, name="user"),
    path("courses/", views.courses, name="courses"),
]
