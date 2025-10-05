from django.urls import path
from .views import (
    ProjectCreateAPIView,
    ProjectUpdateAPIView,
    ProjectDestroyAPIView,
)
app_name='task'
urlpatterns = [
    path('projects/create/', ProjectCreateAPIView.as_view(), name='project-create'),
    path('projects/<int:pk>/update/', ProjectUpdateAPIView.as_view(), name='project-update'),
    path('projects/<int:pk>/delete/', ProjectDestroyAPIView.as_view(), name='project-delete'),
]
