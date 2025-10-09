from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Task ,Log,Notification


@receiver(post_save,sender=Task)
def logs(sender,instance,created,**kwargs):
     user = getattr(instance,'_user',None)
     action = 'created' if created else 'updated'
     print(user)
     if not user :
          return
     
     log=f"{user.email} {action} task #{instance.id}"
     
     Log.objects.create(user=user,task=instance,action=log)



@receiver(post_save,sender=Task)
def notify_task_created(sender,instance,created,**kwargs):
     if created:
          message = f"new task assigned: {instance.title}"
     else:
          message = f"task updated: {instance.status}"

     Notification.objects.create(
          receiver=instance.assigned_to,
          message=message,
     )