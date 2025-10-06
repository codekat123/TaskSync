from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.mixins import ListModelMixin , CreateModelMixin 
from rest_framework.generics import GenericAPIView
from .models import Project , Task
from .serializers import ProjectSerializer , TaskSerializer

class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.select_related('responsible').all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'Manager':
            return self.queryset
        return self.queryset.filter(responsible=user)

    def perform_create(self, serializer):
        user = self.request.user
        if user.role != 'Manager':
            raise PermissionDenied("You're not allowed to create projects.")
        serializer.save(responsible=user)

    def perform_update(self, serializer):
        user = self.request.user
        if user.role != 'Manager':
            raise PermissionDenied("You're not allowed to update projects.")
        serializer.save()

    def perform_destroy(self, instance):
        user = self.request.user
        if user.role != 'Manager':
            raise PermissionDenied("You're not allowed to delete projects.")
        instance.delete()

class TaskAPIView(ListModelMixin,CreateModelMixin,GenericAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(assigned_to=user)

    def get(self, request,*args, **kwargs):
        return self.list(request,*args, **kwargs)
    def post(self, request,*args, **kwargs):
        return self.create(request,*args, **kwargs)
    def put(self, request,*args, **kwargs):
        return self.update(request,*args, **kwargs)
    def delete(self, request,*args, **kwargs):
        return self.destroy(request,*args, **kwargs)