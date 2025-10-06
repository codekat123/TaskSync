from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Task
import json

class TaskConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope['user']
        if not user or not user.is_authenticated:
            await self.close()
            return
        
        self.group_name = "task"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        user = self.scope.get("user")
        if not text_data or not user or not user.is_authenticated:
            return
        
        try:
            payload = json.loads(text_data)
        except json.JSONDecodeError:
            return
        
        task_id = (payload.get('task_id') or '').strip()
        task_status = (payload.get('task_status') or '').strip()

        if not task_id or not task_status:
            return
        
        task = await self.update_task(task_id, task_status)
        if not task:
            await self.send(text_data=json.dumps({'error': 'Task not found'}))
            return

        event = {
            'type': 'task_update',
            'task': {
                'id': task.id,
                'status': task.status,
                'status':'successful'
            }
        }
        await self.channel_layer.group_send(self.group_name, event)

    async def task_update(self, event):
        await self.send(text_data=json.dumps(event['task']))

    # DB helper
    @database_sync_to_async
    def update_task(self, task_id, task_status):
        try:
            task = Task.objects.get(id=task_id)
            task.status = task_status
            task.save()
            return task
        except Task.DoesNotExist:
            return None
