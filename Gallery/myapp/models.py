from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.
class Album(models.Model):
    name = models.CharField(max_length=100,blank=False)
    description = models.CharField(max_length=255,blank=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,related_name='album',default=1)
    cover_image = models.ImageField(upload_to='albums/', blank=True, default='default_cover.jpg')
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering=['-id']

class Image(models.Model):
    title = models.CharField(max_length=100,blank=False)
    description = models.CharField(max_length=255,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/',null=False,blank=False)
    album = models.ForeignKey(Album,on_delete=models.CASCADE,related_name='images',null=False,blank=False,default=1)

def __str__(self):
    return f"{self.title}"

from django.contrib.auth.models import User

class Favorite(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='favorites')
    image=models.ForeignKey(Image,on_delete=models.CASCADE,related_name='favorited_by')
    
def __str__(self):
    return f"{self.user.username} - {self.image.title}"

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics/',default='default.jpg',blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f'{self.user.username}Profile'
    
    def album_count(self):
        return self.user.album.count()
    
    def album_names(self):
        return [album.name for album in self.user.album.all()]
    
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

