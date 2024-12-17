from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required


# Create your views here
def first_page(request):
    return render(request,'myapp/first.html')

def home(request):
    form = None
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('gallery')
        else:
            form = ImageForm()
    return render(request,'myapp/index.html',{'form':form})

def register(request):
    if request.method=="POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Account created successfullly!!!')
            return redirect('login_page')
        else:
            messages.error(request,"Please correct the errors")
    else:
        form=UserCreationForm()
    return render(request,'myapp/register.html',{'form':form})
    
def login_page(request):
    if request.user.is_authenticated:
        return redirect('/home')
    else:
        if request.method == 'POST':
            name = request.POST.get('username')
            pword = request.POST.get('password')
            user = authenticate(request,username=name,password = pword)
            if user is not None:
                login(request,user)
                messages.success(request,'You are logged in!!')
                return redirect('/home')
            else:
                messages.error(request,"Invalid Username or Password")
                return redirect('/login')
    return render(request,'myapp/login.html')

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"You are logged out successfully!!")
    return redirect('/')

from django.db.models import Q
def gallery(request):
    if request.user.is_authenticated:
        album = Album.objects.filter(Q(is_public=True) | Q(owner=request.user))
    else:
        album = Album.objects.filter(is_public=True)
    return render(request, 'myapp/gallery.html', {'album': album})

def create_album(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = AlbumForm(request.POST, request.FILES)
            if form.is_valid():
                album = form.save(commit=False)
                album.owner = request.user
                album.save()
                return redirect('gallery') 
        else:
            form = AlbumForm()
    else:
        return redirect('login_page')
    return render(request, 'myapp/create album.html', {'form': form})

def galleryview(request,album_id):
     album = get_object_or_404(Album, id=album_id)
     images = Image.objects.filter(album=album)  
     return render(request, 'myapp/galleryview.html', {'album': album, 'images': images})

def remove_album(request,album_id):
    if request.user.is_authenticated:
        album = Album.objects.get(id=album_id)
        if album:
            album.delete()
            return redirect('gallery')
        else:
            return redirect('create_album')
    else:
        return redirect('login_page')

         
def favorites(request,image_id):
    if request.user.is_authenticated:
        image = get_object_or_404(Image,id=image_id)
        Favorite.objects.get_or_create(user=request.user,image=image)
        return redirect('favorite_list')
    else:
        return redirect('login_page')

    
def favorite_list(request):
    if request.user.is_authenticated:
        favorites = Favorite.objects.filter(user=request.user)
        return render(request,'myapp/fav.html',{'favorites':favorites})
    else:
        return redirect('login_page')
    
def remove_fav(request,fid):
    if request.user.is_authenticated:
        item = get_object_or_404(Favorite,id=fid,user=request.user)
        item.delete()
        return redirect('favorite_list')
    else:
        return redirect('login_page')

def delete_album(request, album_id):
    if request.user.is_authenticated:
        album = get_object_or_404(Album, id=album_id, owner=request.user)

        if album.is_public:  
            messages.error(request, "The public album cannot be deleted.")
            return redirect('album_list')

        album.delete()
        messages.success(request, "Album deleted successfully.")
        return redirect('album_list')

    return redirect('login')

@login_required
def profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)
    return render(request, 'myapp/profile.html', {'profile': profile})

@login_required
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'myapp/edit_profile.html', {'form': form})

from django.http import JsonResponse


def delete_image(request, image_id):
    if request.method == "POST":
        image = get_object_or_404(Image, id=image_id)
        image.delete()
        messages.success(request, "Image deleted successfully!")
        return redirect('galleryview', album_id=image.album.id)  
    else:
        messages.error(request, "Invalid request method.")
        return redirect('home')  
