import logging
from abc import ABC, abstractmethod
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser

logger = logging.getLogger("__name__")


class BaseConsumer(AsyncWebsocketConsumer, ABC):
    user = None
    room_group_name: str

    async def connect(self):
        if self.scope['user'] == AnonymousUser():
            await self.close()
        else:
            self.user = self.scope['user']
            await self.accept()
            await self.join_group()

    async def disconnect(self, close_code):
        if self.user and hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    @abstractmethod
    async def join_group(self):
        """Phương thức trừu tượng để thêm người dùng vào group."""
        pass

    @abstractmethod
    async def receive(self, text_data=None, bytes_data=None):
        """Phương thức trừu tượng để xử lý tin nhắn từ WebSocket."""
        pass

    @abstractmethod
    async def process_message(self, data):
        """Phương thức trừu tượng để xử lý dữ liệu tin nhắn."""
        pass
