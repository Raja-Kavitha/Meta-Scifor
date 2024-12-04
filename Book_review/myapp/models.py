from django.db import models
import os
import datetime
from django.contrib.auth.models import User

def getFileName(request,filename):
    time = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    new_filename ='%s%s'%(time,filename)
    return os.path.join('Shopcart/static/uploads/',new_filename)


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    genre = models.CharField(max_length=200)
    summary = models.TextField(null=True)
    image = models.ImageField(upload_to=getFileName,null=True,blank=True)
    
def __str__(self):
    return self.title

# class CustomUser(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.CharField(max_length=50)
#     mobile_no = models.CharField(max_length=10)

# def __str__(self):
#     return self.name


class Review(models.Model):
    book = models.ForeignKey(Book,on_delete=models.CASCADE,related_name='reviews')
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i,i)for i in range(1,6)])
    comment = models.TextField()
    date = models.TimeField(auto_now_add=True)

def __str__(self):
    return f"{self.user.name}-{self.book.title} ({self.rating})"

class Wishlist(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    
def __str__(self):
    return f"{self.user.username}'s wishlist for {self.book.title}"