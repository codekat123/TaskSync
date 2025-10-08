from django.contrib import admin
from django.urls import path , include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/',include('account.urls',namespace='account')),
    path('task/',include('task_management.urls',namespace='task')),
    path('notification/',include('notification.urls',namespace='notification')),
]
