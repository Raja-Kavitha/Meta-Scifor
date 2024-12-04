from django.db import models
import datetime
import os
from django.contrib.auth.models import User

def getFileName(request,filename):
    time = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    new_filename ='%s%s'%(time,filename)
    return os.path.join('uploads/',new_filename)

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=150,null=False,blank =False)
    image = models.ImageField(upload_to=getFileName,null= True,blank=True)
    decription = models.TextField(max_length=500,null=False,blank=False)
    status = models.BooleanField(default=False,help_text='0-show,1-Hidden')
    created_at = models.DateTimeField(auto_now_add=True)

def __str__(self):
    return self.name

class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=150,null=False,blank =False)
    product_image = models.ImageField(upload_to=getFileName,null= True,blank=True)
    quantity = models.IntegerField(null=False,blank=False)
    original_price = models.FloatField(null=False,blank=False)
    selling_price = models.FloatField(null=False,blank=False)
    description = models.TextField(max_length=500,null=False,blank=False)
    status = models.BooleanField(default=False,help_text='0-show,1-Hidden')
    trending= models.BooleanField(default=False,help_text='0-default,1-Trending')
    created_at = models.DateTimeField(auto_now_add=True)
    vendor = models.CharField(max_length=150,null=False,blank =False)

def __str__(self):
    return self.name


# class Cart(models.Model):
#     Name=models.CharField(max_length=30)
#     Address=models.TextField()
#     Phone_number =models.CharField(max_length=10)
#     product_id =models.ForeignKey(Product,on_delete=models.CASCADE)


# class Save_item(models.Model):
#     user=models.ForeignKey(User,on_delete=models.CASCADE)
#     product=models.ForeignKey(Product,on_delete=models.CASCADE)
#     product_qty=models.IntegerField(null=False,default=1,blank=False)


# class Saved_items(models.Model):
#     user=models.ForeignKey(User,on_delete=models.CASCADE)
#     product=models.ForeignKey(Product,on_delete=models.CASCADE)
#     product_qty=models.IntegerField(null=False,default=1,blank=False)

from django.contrib.auth.models import User

class Cart_items(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_qty = models.IntegerField(null=False, default=1, blank=False)

    @property
    def total_cost(self):
        return self.product_qty * self.product.selling_price  
    
class Favourite(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
