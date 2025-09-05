from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "status", "priority", "due_date"]
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }


class TaskFilterForm(forms.Form):
    STATUS_CHOICES = [
        ("", "All"),
        ("todo", "To Do"),
        ("in_progress", "In Progress"),
        ("done", "Done"),
        ]
    
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False, label="Status")

class CommentForm(forms.ModelForm):
  class Meta:
    model = Comment
    fields = ['content', 'media']
    widgets = {
       'media': forms.FileInput
    }

class SimpleRegisterForm(UserCreationForm):
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"class": "input-field", "placeholder": "Введите пароль"})
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={"class": "input-field", "placeholder": "Повторите пароль"})
    )

    class Meta:
        model = User
        fields = ["username", "password1", "password2"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "input-field", "placeholder": "Введите логин"}),
        }


class SimpleLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "input-field", "placeholder": "Введите логин"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "input-field", "placeholder": "Введите пароль"})
    )
