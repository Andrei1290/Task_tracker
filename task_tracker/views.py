from django.shortcuts import render, redirect
from task_tracker import models
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import TaskForm, CommentForm, TaskFilterForm, SimpleRegisterForm, SimpleLoginForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixin import UserIsOwnerMixin
from django.core.exceptions import PermissionDenied
from django.contrib.auth.views import LoginView, LogoutView

from django.contrib.auth.forms import UserCreationForm
from django.views import generic

from django.contrib.auth.decorators import login_required

from django.views import View
from django.shortcuts import get_object_or_404

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
    

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = models.Task
    form_class = TaskForm
    template_name = "task_tracker/task_form.html"  # шаблон, где будет форма
    success_url = reverse_lazy("task-list")  # после сохранения вернёт на список задач

    def form_valid(self, form):
        form.instance.creator = self.request.user  # автор автоматически = текущий юзер
        return super().form_valid(form)

class TaskUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = models.Task
    form_class = TaskForm
    success_url = reverse_lazy('task-list')

class TaskCompleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(models.Task, pk=pk)
        if task.creator != request.user:
            raise PermissionDenied("Вы не автор этой задачи!")
        task.status = "done"
        task.save()
        return redirect("task-detail", pk=task.pk)
    
class TaskUpdateStatusView(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(models.Task, pk=pk)
        if task.creator != request.user:
            raise PermissionDenied("Вы не автор этой задачи!")
        new_status = request.POST.get("status")
        if new_status in dict(models.Task.STATUS_CHOICES).keys():
            task.status = new_status
            task.save()
        return redirect("task-detail", pk=task.pk)

class TaskDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = models.Task
    success_url = reverse_lazy('task-list')



class CommentUpdateView(UpdateView):
    model = models.Comment
    fields = ["content"]

    def form_valid(self, form):
        comment = self.get_object()
        if comment.author != self.request.user:
            raise PermissionDenied("Вы не являетесь автором коментария!")
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('task-detail', kwargs={'pk':self.object.task.pk})
    def dispatch(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.author != request.user:
            raise PermissionDenied("Вы не автор этого комментария!")
        return super().dispatch(request, *args, **kwargs)

    

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
    template_name = 'task_tracker/login.html'
    authentication_form = SimpleLoginForm  # <--- вот это


class CustomLogoutView(LogoutView):
    next_page = 'login'



class RegisterView(generic.CreateView):
    form_class = SimpleRegisterForm
    template_name = "task_tracker/register.html"
    success_url = reverse_lazy("login")

