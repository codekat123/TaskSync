from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from rest_framework.exceptions import PermissionDenied
from .models import Project, Task , Notification
from .serializers import ProjectSerializer, TaskSerializer,NotificationSerializer
from .permission import IsManager


# -------- Manager Projects --------
class ManagerProjectListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsManager]
    throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        user = self.request.user
        return Project.objects.select_related('manager').filter(manager=user)

    def perform_create(self, serializer):
        serializer.save(manager=self.request.user)


class ManagerProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsManager]
    throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        user = self.request.user
        return Project.objects.select_related('manager').filter(manager=user)


# -------- Tasks --------
class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]



    def get_queryset(self):
        user = self.request.user
        role = getattr(user, "role", None)
    
        filters = {
            "Manager": {"project__manager": user},
            "teamleader": {"project__teamleader": user},
            "Employee": {"assigned_to": user},
        }
    
        return Task.objects.filter(**filters.get(role, {}))


    def perform_create(self, serializer):
        user = self.request.user
        if user.role in ["Manager", "teamleader"]:
            instance = serializer.save()
            instance._user = user  
            instance.save()
        else:
            raise PermissionDenied("You don’t have permission to create tasks.")


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
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
    
    def perform_update(self, serializer):
        instance = serializer.save()
        instance._user = self.request.user
        instance.save()



class IndividualNotificaiton(generics.ListAPIView):
     queryset = Notification.objects.all()
     serializer_class = NotificationSerializer


