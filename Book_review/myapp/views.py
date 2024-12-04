from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from myapp.forms import CustomUserForm
from django.http import JsonResponse
import json

# Create your views here.
def home(request):
    return render(request,'myapp/index.html')

def book_list(request):
    books=Book.objects.all()
    return render (request,'myapp/book_list.html',{'books':books})

def book_detail(request,id):
    book=get_object_or_404(Book,id=id)
    return render (request,'myapp/book_detail.html',{'book':book})

def book_review(request, id):
    book = get_object_or_404(Book, id=id)
    reviews = Review.objects.filter(book=book)
    return render(request, 'myapp/reviews.html', {'book': book,'reviews': reviews})

def login_page(request):
    if request.user.is_authenticated:
         return redirect('/')
    else:
        if request.method == 'POST':
            username=request.POST.get('username')
            pword=request.POST.get('password')
            user= authenticate(request,username=username,password=pword)
            if user is not None:
                login(request,user)
                messages.success(request,'You are logged in successfully!!')
                return redirect('/')
            else:
                messages.error(request,"Invalid Username or Password")
                return redirect('/login_page')
        return render(request,'myapp/login.html')

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,'You are logged out successfully!!')
        return redirect('/')
    
# from django.contrib.auth.forms import UserCreationForm

# from django.contrib.auth.models import User
# from django.shortcuts import render, redirect
# from django.contrib import messages
# from .forms import CustomUserForm

# def register(request):
#     form = CustomUserForm()
#     if request.method == "POST":
#         form = CustomUserForm(request.POST)
#         if form.is_valid():
#             # Save the user and populate the username field correctly
#             user = form.save(commit=False)
#             user.name = form.cleaned_data.get('name')  # Ensure username is set
#             user.email = form.cleaned_data.get('email')  # Ensure email is set
#             messages.success(request, "Registration successful! Please log in.")
#             return redirect('/login_page')
#     return render(request, 'myapp/register.html', {'form': form})

from django.contrib.auth.models import User

def register(request):
    form = CustomUserForm()
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists.")
            else:
                form.save()
                messages.success(request, "Registration successful! Please log in.")
                return redirect('/login_page')
    return render(request, 'myapp/register.html', {'form': form})


def add_review(request,id):
    book = get_object_or_404(Book,id=id)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        Review.objects.create(
            book=book,
            user = request.user,
            rating = rating,
            comment = comment
        )
        messages.success(request,'Review added successfully!!!')
        return redirect('book_review',id=book.id)
    return render(request,'myapp/add_review.html',{'book':book})

def wish_page(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.loads(request.body)
            book_id = data.get('book_id')
            if Wishlist.objects.filter(user=request.user,book_id =book_id).exists():
                return JsonResponse({'status': 'Product already in Wishlist'},status=200)
            else:
                book = get_object_or_404(Book,id=book_id)
                Wishlist.objects.create(user=request.user,book=book)
                return JsonResponse({'status': 'Product added to Wishlist'})
        else:
            return JsonResponse({'status':'Login to add item to Wishlist'},status=200)
    else:
        return JsonResponse({'status':'Invalid Access'},status=200)
    
def wishlist(request):
    if request.user.is_authenticated:
        wish=Wishlist.objects.filter(user=request.user)
        return render(request,'myapp/wishlist.html',{'wish':wish})
    else:
        return redirect('/login_page')

def remove_wishlist(request,fid):
    if request.user.is_authenticated:
        item =Wishlist.objects.get(id=fid,user=request.user)
        if item:
            item.delete()
        return redirect('/wishlist')
    else:
        return redirect('/login_page')