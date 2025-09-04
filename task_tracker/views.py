from django.shortcuts import render, redirect
from task_tracker import models
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import TaskForm, CommentForm, TaskFilterForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixin import UserIsOwnerMixin
from django.core.exceptions import PermissionDenied
from django.contrib.auth.views import LoginView, LogoutView

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

    def get_context_data(self, **kwargs):   
        context = super().get_context_data(**kwargs)
        context["comment_form"] = CommentForm()
        return context
    
    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST, request.FILES)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.task = self.get_object()
            comment.save()
            return redirect('task-detail', pk=comment.task.pk)
    

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

class CommentUpdateView(UpdateView):
    model = models.Comment
    fields = ["content"]

    def from_valid(self, form):
        comment = self.get_object()
        if comment.author != self.request.user:
            raise PermissionDenied("Вы не являетесь автором коментария!")
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('task-detail', kwargs={'pk':self.object.task.pk})
    

class CommentDeleteView(DeleteView):
    model = models.Comment

    success_url = reverse_lazy('task-list')

    def get_success_url(self):
        return reverse_lazy('task-detail', kwargs={'pk':self.object.task.pk})

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != request.user:
            raise PermissionDenied("Вы не автор этого комментария!")
        return super().dispatch(request, *args, **kwargs)
    

class CustomLoginView(LoginView):
    redirect_authenticated_user = True
    template_name='task_tracker/login.html'


class CustomLogoutView(LogoutView):
    next_page = 'login'