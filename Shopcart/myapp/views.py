from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib import messages
from myapp.forms import CustomUserForm
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
import json

# Create your views here.
def home(request):
    products = Product.objects.filter(trending=1)
    return render(request,'myapp/index.html',{'products':products})

def login_page(request):
    if request.user.is_authenticated:
         return redirect('/')
    else:
        if request.method == 'POST':
            name=request.POST.get('username')
            pword=request.POST.get('password')
            user= authenticate(request,username=name,password=pword)
            if user is not None:
                login(request,user)
                messages.success(request,'You are logged in successfully!!')
                return redirect('/')
            else:
                messages.error(request,"Invalid Username or Password")
                return redirect('/login')
        return render(request,'myapp/login.html')

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,'You are logged out successfully!!')
        return redirect('/')

def register(request):
    form = CustomUserForm()
    if request.method =='POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Registration successful you can login now!!')
            return redirect('/login')
    return render(request,'myapp/register.html',{'form':form})

def collections(request):
    category = Category.objects.filter(status=0)
    return render(request,'myapp/collections.html',{'category':category})


def collectionsview(request, name):
    if (Category.objects.filter(name= name,status=0)):
         products = Product.objects.filter(category__name=name)
         return render(request,'myapp/products/index.html',{'products':products,'category_name':name})
    else:
        messages.warning(request,'No such category found')
        return redirect('collections')
    
def product_details(request,cname,pname):
    if(Category.objects.filter(name=cname,status=0)):
        if(Product.objects.filter(name=pname,status=0)):
            products= Product.objects.filter(name=pname,status=0).first()
            return render (request,'myapp/products/product_details.html',{'products':products})
        else:
            messages.error(request,'No such product found')
            return redirect('collections')
    else:
        messages.error(request,'No such category found')
        return redirect('collections')
    
def add_to_cart(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_qty = data['product_qty']
            product_id = data['pid']
            product_status = Product.objects.get(id=product_id)
            if product_status:
                if Cart_items.objects.filter(user=request.user,product_id =product_id):
                    return JsonResponse({'status': 'Product already in Cart'},status=200)
                else:
                    if product_status.quantity >= product_qty:
                        Cart_items.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
                        return JsonResponse({'status':'Product added to cart'},status=200)
                    else:
                        return JsonResponse({'status':'Product is out of stock'},status=200)
        else:
            return JsonResponse({'status':'Login to add cart'},status=200)
    else:
        return JsonResponse({'status':'Invalid Access'},status=200)
    
def cart_page(request):
        if request.user.is_authenticated:
            cart=Cart_items.objects.filter(user=request.user)
            return render(request,'myapp/cart.html',{'cart':cart})

        else:
            return redirect('/')

def remove_cart(request,cid):
    cart_item =Cart_items.objects.get(id=cid)
    cart_item.delete()
    return redirect('/cart')

def fav_page(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_id = data['pid']
            product_status = Product.objects.get(id=product_id)
            if product_status:
                if Favourite.objects.filter(user=request.user,product_id =product_id):
                    return JsonResponse({'status': 'Product already in Favourite'},status=200)
                else:
                    Favourite.objects.create(user=request.user,product_id=product_id)
                    return JsonResponse({'status': 'Product added to favourites'})
        else:
            return JsonResponse({'status':'Login to add item to favourite'},status=200)
    else:
        return JsonResponse({'status':'Invalid Access'},status=200)
    
def favviewpage(request):
    if request.user.is_authenticated:
        fav=Favourite.objects.filter(user=request.user)
        return render(request,'myapp/fav.html',{'fav':fav})

    else:
        return redirect('/')
    
def remove_fav(request,fid):
    item =Favourite.objects.get(id=fid)
    item.delete()
    return redirect('/favviewpage')