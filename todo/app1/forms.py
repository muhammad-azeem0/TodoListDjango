# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from .models import Task



class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'CNIC','age' ,'address')
        labels = {'email': 'Email', 'phone_number': 'Phone No.'}


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email',)




class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline', 'completed']