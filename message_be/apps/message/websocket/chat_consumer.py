import json
import logging

from django.contrib.auth import get_user_model

from .base_consumer import BaseConsumer

logger = logging.getLogger("__name__")
User = get_user_model()


class ChatConsumer(BaseConsumer):
    room_group_name: str

    async def join_group(self):
        """add user to group chat"""
        self.room_group_name = f'chat_{self.user.id}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        """Receive data from WebSocket"""
        try:
            data = json.loads(text_data)
            print("Data received from FE:", data)
            await self.process_message(data)
        except Exception as e:
            logger.exception("Error in receive: %s", e)

    async def process_message(self, data):
        """handle messages chat"""
        message = data['message']
        sender = self.user
        recipient_id = data['recipient']

        recipient = await User.objects.filter(id=recipient_id).afirst()
        if recipient:
            response = {
                'sender': str(sender),
                'recipient': str(recipient),
                'message': message,
            }

            await self.channel_layer.group_send(
                f"chat_{recipient.id}",
                {
                    'type': 'chat_message',
                    'message': response
                }
            )

    async def chat_message(self, event):
        """Send messages to WebSocket"""
        message = event['message']
        await self.send(text_data=json.dumps(message))
