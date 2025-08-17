from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Task(models.Model):
    STATUS_CHOICES = [
        ("todo", "To Do"),
        ("in_progress", "In Progress"),
        ("done", "Done"),
        ]
    
    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ]

    title = models.CharField(max_length=63)
    description = models.TextField()
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='todo')
    priority = models.CharField(max_length=25, choices=PRIORITY_CHOICES, default='medium')
    due_date = models.DateTimeField(null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return self.title