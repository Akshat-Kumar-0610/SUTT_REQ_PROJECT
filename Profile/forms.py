from django import forms
from django.contrib.auth.models import User
from .models import Profile
class UserUpdateForm(forms.ModelForm):
    first_name=forms.CharField(label='First Name')
    last_name=forms.CharField(label='last Name',required=False)
    
    class Meta:
        model=User
        fields =['username','first_name','last_name']

class ProfileUpdateForm(forms.ModelForm):
    bio=forms.CharField(label='bio',required= False)
    class Meta:
        model=Profile
        fields =['bio','image']

