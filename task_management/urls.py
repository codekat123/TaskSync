from django.urls import path
from .views import (
    ManagerProjectListCreateView,
    ManagerProjectDetailView,
    TaskListCreateView,
    TaskDetailView,
)

app_name = 'task'

urlpatterns = [
    # Manager Projects
    path('manager/projects/', ManagerProjectListCreateView.as_view(), name='manager-project-list-create'),
    path('manager/projects/<int:pk>/', ManagerProjectDetailView.as_view(), name='manager-project-detail'),

    # Tasks
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
]
