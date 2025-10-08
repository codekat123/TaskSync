from django.db import models
from account.models import User


class Notification(models.Model):
     user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="notifications")
     message = models.TextField()
     is_read = models.BooleanField(default=False)
     created_at = models.DateTimeField(auto_now_add=True)

