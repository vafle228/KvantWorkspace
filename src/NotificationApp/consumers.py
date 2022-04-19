import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        user_id = self.scope['user'].id
        self.room_group_name = f'notification_{user_id}'
            
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name)

    def user_notification(self, event):
        self.send(text_data=json.dumps({
            'title': event.get('title'),
            'image_url': event.get('image_url'),
            'description': event.get('description'),
            'object_name': event.get('object_name'),
            'redirect_link': event.get('redirect_link'),
        }))
