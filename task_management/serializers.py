from rest_framework import serializers
from .models import Task , Project

class TaskSerializer(serializers.ModelSerializer):
     class Meta:
          model = Task
          fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    completed = serializers.SerializerMethodField()
    in_progress = serializers.SerializerMethodField()
    pending = serializers.SerializerMethodField()
    cancelled = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'due_date', 'responsible',
            'completed', 'in_progress', 'pending', 'cancelled'
        ]

    def get_completed(self, obj):
        return obj.completed()

    def get_in_progress(self, obj):
        return obj.in_progress()

    def get_pending(self, obj):
        return obj.pending()

    def get_cancelled(self, obj):
        return obj.cancelled()

    def remaining_days(self,obj):
        return obj.remaining_days()