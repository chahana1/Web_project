from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import check_password
from django import forms
from .models import User,Profile

class UserForm(UserCreationForm):
    class Meta():
        model = User
        fields = ['email','name','gender']


class RegisterForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ["address","pet_name","birth", "image", "char"]
        