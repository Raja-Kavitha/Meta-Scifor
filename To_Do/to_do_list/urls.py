from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('delete/<str:task>/', views.delete_task, name='delete_task'),
]
