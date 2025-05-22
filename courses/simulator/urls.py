from django.urls import path
from . import views

app_name = 'simulator'

urlpatterns = [
    path('simulate/', views.simulate, name='simulate'),
] 