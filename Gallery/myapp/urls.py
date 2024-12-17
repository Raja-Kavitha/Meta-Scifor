from django.urls import path
from . import views

urlpatterns = [
    path('',views.first_page,name='first_page'),
    path('home',views.home,name='home'),
    path('register/',views.register,name='register'),
    path('login_page/',views.login_page,name='login_page'),
    path('logout_page/',views.logout_page,name='logout_page'),
    path('create_album/',views.create_album,name='create_album'),
    path('gallery/',views.gallery,name='gallery'),
    path('gallery/<int:album_id>/',views.galleryview,name='galleryview'),
    path('remove_album/<int:album_id>/', views.remove_album, name='remove_album'),
    path('favorites/<int:image_id>/',views.favorites,name='favorites'),
    path('favorite_list/',views.favorite_list,name='favorite_list'),
    path('remove_fav/<int:fid>/',views.remove_fav,name='remove_fav'),
    path('profile/',views.profile,name='profile'),
    path('edit_profile/',views.edit_profile,name='edit_profile'),
    path('delete_image/<int:image_id>/', views.delete_image, name='delete_image'),


]
