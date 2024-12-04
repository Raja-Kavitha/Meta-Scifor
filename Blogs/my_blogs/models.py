from django.db import models

# Create your models here.
class Blog(models.Model):
    title= models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateField()
    writer = models.CharField(max_length=15)

def __str__(self):
    return self.title