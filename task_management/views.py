from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated , AllowAny
from rest_framework.throttling import UserRateThrottle
from rest_framework.exceptions import PermissionDenied

from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer
from .permission import IsManager, IsTeamLeader, IsEmployee


class ManagerProjectViewSet(ModelViewSet):

    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsManager]
    throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        user = self.request.user
        return Project.objects.select_related('manager').filter(manager=user)

    def perform_create(self, serializer):
        serializer.save(manager=self.request.user)


class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        user = self.request.user

        if user.role == "Manager":
            return Task.objects.filter(project__manager=user)

        elif user.role == "teamleader":
            return Task.objects.filter(project__teamleader=user)

        elif user.role == "Employee":
            return Task.objects.filter(assigned_to=user)
        return Task.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if user.role in ["Manager", "teamleader"]:
            serializer.save()
        else:
            raise PermissionDenied("You don’t have permission to create tasks.")
        
        
    
