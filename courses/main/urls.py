from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("reg/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("courses/", views.courses_overview, name="courses"),
    path("courses/<int:course_id>", views.course_page, name="course_page"),
    path("courses/<int:course_id>/lesson/<int:lesson_id>", views.lesson_page, name="lesson_page"),
    path("courses/<int:course_id>/test/<int:question_id>", views.question_page, name="question page"),
    path("test", views.test_page, name="test page")
]
