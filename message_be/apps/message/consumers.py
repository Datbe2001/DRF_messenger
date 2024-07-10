import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

User = get_user_model()
logger = logging.getLogger("__name__")


class ChatConsumer(AsyncWebsocketConsumer):
    user: User
    room_group_name: str

    async def connect(self):
        if self.scope['user'] == AnonymousUser():
            await self.close()
        else:
            self.user = self.scope['user']
            self.room_group_name = f'chat_{self.user.id}'

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()

    async def disconnect(self, close_code):
        if self.scope['user'] != AnonymousUser():
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data=None, bytes_data=None):
        try:
            data = json.loads(text_data)
            message = data['message']
            sender = self.user
            recipient_id = data['recipient']

            recipient = await User.objects.filter(id=recipient_id).afirst()
            if recipient:
                response = {
                    'sender': str(sender.id),
                    'recipient': str(recipient_id),
                    'message': message,
                    'user_recipient': {
                        'id': str(recipient.id),
                        'username': str(recipient.username),
                        'full_name': str(recipient.full_name),
                        'email': str(recipient.email),
                    }
                }

                print('Websocket consumer connected successfully', response)

                await self.channel_layer.group_send(
                    f"chat_{recipient.id}",
                    {
                        'type': 'chat_message',
                        'message': response
                    }
                )
        except Exception as e:
            logger.exception("Unexpected error: %s", e)

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))
