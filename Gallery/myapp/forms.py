from django import forms
from .models import *

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'description', 'image', 'album']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter image title'
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Add a description...'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'album': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
        
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['album'].queryset =Album.objects.all()
        self.fields['album'].empty_label = "Create New Album"


class AlbumForm(forms.ModelForm):
    class Meta():
        model = Album
        fields =['name','description','cover_image','is_public']
        widgets = {
            'name':forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder':'Enter title'
            }),
            'description':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Add a description'
            }),
            'cover_image':forms.ClearableFileInput(attrs={
                'class':'form-control'
            }),
            'is_public':forms.CheckboxInput(attrs={
                'class':'form-check-input',

            })
            
        }
        def clean_cover_image(self):
            cover_image = self.cleaned_data.get('cover_image')
            if cover_image and not cover_image.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                raise forms.ValidationError("Only .png, .jpg, and .jpeg files are allowed.")
            return cover_image
    

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm your password'})
        }

class LoginForm(forms.Form):
    class Meta:
        fields = ['username','password']
        widgets = {
            'username': forms.TextInput(attrs={
                'class':'form-control',
                'placeholder': 'Enter Username'
            }),
            'password':forms.PasswordInput(attrs={
                'class':'form-control',
                'placeholder':'Enter password'
            })
        }    

from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic', 'bio']  
        widgets = {
            'profile_pic':forms.ClearableFileInput(attrs={
                'class':'form-control'
            }),
            'bio':forms.Textarea(attrs={
                'class': 'form-control',
                'row':2
            })
        }
