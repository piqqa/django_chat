from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from chat.models import Room, Message
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name ='empty'
        if self.scope["user"].is_anonymous:
            self.close()
            return
        self.username = self.scope["user"].username
        if self.checked_privacy():

            try:
                self.room = Room.objects.get(name=self.room_name)
            except ObjectDoesNotExist:
                self.room = Room(name=self.room_name)
                self.room.save()

            self.room_name = self.room_name.replace('|','_')
            self.room_group_name = 'chat_%s' % self.room_name

            # Join room group
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )

            self.accept()

    def checked_privacy(self):
        return True

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        user = self.scope["user"]#User.objects.get(username='test')
        record = Message(room=self.room, text=message, user=user)
        record.save()
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': self.username,
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))


class PrivateChatConsumer(ChatConsumer):
    def checked_privacy(self):
        if self.username not in self.room_name.split('|'):
            print(self.scope["user"])
            print(self.username)
            print(self.room_name)
            self.close()
            return False
        return True
