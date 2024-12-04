from django.shortcuts import render
from my_blogs.models import Blog

# Create your views here.
def blog(request):
    blogs = Blog.objects.all()
    return render(request,'my_blogs/index.html',{'blogs':blogs})