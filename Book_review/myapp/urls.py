from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name='home'),
    path('register/', views.register, name='register'),
    path('login_page/', views.login_page, name='login_page'), 
    path('logout_page/', views.logout_page, name='logout_page'), 
    path('books/',views.book_list,name='book_list'),
    path('books/<int:id>/', views.book_detail, name='book_detail'), 
    path('books/<int:id>/review/', views.book_review, name='book_review'), 
    path('books/<int:id>/add_review/', views.add_review, name='add_review'),
    path('wish/',views.wish_page,name='wish_page'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('remove_wishlist/<int:fid>/', views.remove_wishlist, name='remove_wishlist'),

]
