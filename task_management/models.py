from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
User = get_user_model()

class Project(models.Model):
     name = models.CharField(max_length=100)
     description = models.TextField(max_length=500)
     due_date = models.DateField(default=timezone.now)
     responsible = models.ForeignKey(User,on_delete=models.DO_NOTHING)

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
