from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    teamleader = models.ForeignKey(User, on_delete=models.DO_NOTHING,related_name='teamleader')
    manager = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def completed(self):
        total_tasks = Task.objects.filter(project=self).count()
        completed_tasks = Task.objects.filter(project=self, status='COMPLETED').count()
        if total_tasks == 0:
            return "there's no tasks yet!"
        return round((completed_tasks / total_tasks) * 100, 2)

    def in_progress(self):
        total_tasks = Task.objects.filter(project=self).count()
        inprogress_tasks = Task.objects.filter(project=self, status='IN_PROGRESS').count()
        if total_tasks == 0:
            return "there's no tasks yet!"
        return round((inprogress_tasks / total_tasks) * 100, 2)

    def pending(self):
        total_tasks = Task.objects.filter(project=self).count()
        pending_tasks = Task.objects.filter(project=self, status='PENDING').count()
        if total_tasks == 0:
            return "there's no tasks yet!"
        return round((pending_tasks / total_tasks) * 100, 2)

    def cancelled(self):
        total_tasks = Task.objects.filter(project=self).count()
        cancelled_tasks = Task.objects.filter(project=self, status='CANCELLED').count()
        if total_tasks == 0:
            return "there's no tasks yet!"
        return round((cancelled_tasks / total_tasks) * 100, 2)
    
    def remaining_days(self):
        return (self.due_date - timezone.now().date()).days



class Task(models.Model):
     STATUS_CHOICES = [
             ('PENDING', 'Pending'),
             ('IN_PROGRESS', 'In Progress'),
             ('COMPLETED', 'Completed'),
             ('CANCELLED', 'Cancelled'),
         ]
     PRIORITY_CHOICES = [(i, str(i)) for i in range(1, 11)]
     
     assigned_to = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='tasks')
     project = models.ForeignKey(Project,on_delete=models.CASCADE,related_name='tasks')
     title = models.CharField(max_length=255)
     description = models.TextField(blank=True)
     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
     priority = models.PositiveIntegerField(choices=PRIORITY_CHOICES)
     due_date = models.DateField()
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)

     def __str__(self):
         return f"{self.title} ({self.status})"



class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    action = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)


class Notification(models.Model):
     receiver = models.ForeignKey(User,on_delete=models.CASCADE,related_name="notifications")
     message = models.TextField()
     is_read = models.BooleanField(default=False)
     created_at = models.DateTimeField(auto_now_add=True)