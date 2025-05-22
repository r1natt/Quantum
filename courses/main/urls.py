from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("reg/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("calc_loss/", views.calc_loss, name="loss"),
    path("calc_photo/", views.calc_photo, name="photo"),
    path("calcs/", views.calcs_page, name="calcs"), 
    path("courses/", views.courses_overview, name="courses"),
    path("courses/<int:course_id>", views.course_intro, name="course_page"),
    path("courses/<int:course_id>/structure", views.course_page, name="course_page"),
    path("courses/<int:course_id>/test/intro", views.test_intro, name="course_page"),
    path("courses/<int:course_id>/lesson/<int:lesson_id>", views.lesson_page, name="lesson_page"),
    path("courses/<int:course_id>/test/<int:question_id>", views.question_page, name="question page"),
    path("courses/<int:course_id>/test/results", views.test_results_page, name="test results"),
    path("tasks/", views.tasks_overview, name="tasks_overview"),
    path("tasks/<int:task_group_id>", views.task_page, name="task_page"),
    path("tasks/<int:task_group_id>/<int:task_id>", views.task, name="task"),

    path("test", views.test_page, name="test page")
]
