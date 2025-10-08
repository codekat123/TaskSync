from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification
from task_management.models import Project , Task

@receiver(post_save,sender=Task)
def notify_task_created(sender,instance,created,**kwargs):
     if created:
          message = f"new task assigned: {instance.title}"
     else:
          message = f"task updated: {instance.status}"

     Notification.objects.create(
          user=instance.assigned_to,
          message=message,
     )
     