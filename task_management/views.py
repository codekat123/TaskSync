from django.shortcuts import render
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, ListAPIView
from .models import Task , Project
from .serializers import TaskSerializer , ProjectSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

class ProjectCreateAPIView(CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if user.role != 'Manager':
            raise ValidationError("You're not allowed to do this.")
        
        serializer.save(responsible=user)


class ProjectUpdateAPIView(UpdateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        user = self.request.user
        if user.role != 'Manager':
            raise ValidationError("You're not allowed to do this.")
        
        serializer.save(responsible=user)


class ProjectDestroyAPIView(DestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        user = self.request.user
        if user.role != 'Manager':
            raise ValidationError("You're not allowed to do this.")
        
        instance.delete()
     

