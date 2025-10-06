from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from .models import Task
from django.conf import settings

@shared_task
def send_due_soon_reminders():
    tomorrow = timezone.now() + timedelta(days=1)
    tasks = Task.objects.filter(due_date__lte=tomorrow, due_date__gte=timezone.now())

    for task in tasks:
        if task.assigned_to and task.assigned_to.email:
            send_mail(
                subject=f"Reminder: {task.title} is due soon!",
                message=f"Hey {task.assigned_to.first_name},\n\nJust a heads-up that your task '{task.title}' is due soon (due on {task.due_date}).\n\nStay productive 💪",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[task.assigned_to.email],
                fail_silently=False,
            )