from django.urls import path
from . import views

urlpatterns=[
    path('blogs/',views.blog,name='blog'),
]