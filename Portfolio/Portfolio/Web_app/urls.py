from django.urls import path
from Web_app import views

urlpatterns = [
    path('', views.HomePage,name='home'),
]

