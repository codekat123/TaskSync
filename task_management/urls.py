from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *


app_name='task'

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
urlpatterns = router.urls
urlpatterns += [
    path('tasks/', TaskAPIView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskAPIView.as_view(), name='task-detail'),]
