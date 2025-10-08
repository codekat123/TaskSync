from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ManagerProjectViewSet, TaskViewSet

app_name = 'task'

router = DefaultRouter()
router.register(r'manager/projects', ManagerProjectViewSet, basename='manager-project')
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('', include(router.urls)),
]
