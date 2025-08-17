from django.shortcuts import render
from task_tracker import models
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import TaskForm, TaskFilterForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixin import UserIsOwnerMixin

# Create your views here.

class TaskListView(ListView):
    model = models.Task
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get("status", "")
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def get_context_data(self, **kwargs):   
        context = super().get_context_data(**kwargs)
        context["form"] = TaskFilterForm(self.request.GET)
        return context


class TaskDetailView(DetailView):
    model = models.Task
    context_object_name = 'task'

class TaskCreateView(CreateView):
    model = models.Task
    success_url = reverse_lazy('tast-list')
    
    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

class TaskUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = models.Task
    form_class = TaskForm
    success_url = reverse_lazy('task-list')

class TaskDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = models.Task
    success_url = reverse_lazy('task-list')


