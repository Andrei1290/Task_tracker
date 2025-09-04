from django import forms
from .models import *

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