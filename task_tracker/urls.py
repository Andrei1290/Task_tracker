from django.urls import path
from task_tracker import views

urlpatterns = [
    path('', views.TaskListView.as_view(), name='task-list'),
    path('<int:pk>/', views.TaskDetailView.as_view(), name='task-detail'),
    path('tast_create', views.TaskCreateView.as_view(), name='task-create'),
    path('update/<int:pk>/', views.TaskUpdateView.as_view(), name='task-update'),
    path('delete/<int:pk>/', views.TaskDeleteView.as_view(), name='task-delete'),
    path('comment_update/<int:pk>/', views.CommentUpdateView.as_view(), name='comment-update'),
    path('comment_delete/<int:pk>/', views.CommentDeleteView.as_view(), name='comment-delete'),
    path('login', views.CustomLoginView.as_view(), name='login'),
    path('logout', views.CustomLogoutView.as_view(), name='logout'),
    path("register", views.RegisterView.as_view(), name="register"),
]
