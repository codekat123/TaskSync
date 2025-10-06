from django.urls import path
from task_management.routing import websocket_urlpatterns as task_ws

websocket_urlpatterns = [
    *task_ws,
]
