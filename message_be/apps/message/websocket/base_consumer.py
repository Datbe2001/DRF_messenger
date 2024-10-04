import logging
from abc import ABC, abstractmethod
from typing import Optional

import redis
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

User = get_user_model()
logger = logging.getLogger("__name__")
redis_instance = redis.StrictRedis(host='localhost', port=6379, db=0)


class BaseConsumer(AsyncWebsocketConsumer, ABC):
    user: Optional[User] = None
    room_group_name: Optional[str] = None

    async def connect(self):
        """Connect Websocket."""
        if self.scope['user'] == AnonymousUser():
            await self.close()
        else:
            self.user = self.scope['user']
            await self.accept()
            await self.join_group()
            await self.enable_user_active_state()

    async def disconnect(self, close_code):
        """Disconnect Websocket."""
        if self.user and hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
            await self.disable_user_active_state()

    @abstractmethod
    async def join_group(self):
        """Abstract method to add user to group."""
        pass

    @abstractmethod
    async def receive(self, text_data=None, bytes_data=None):
        """Abstract method for handling data from WebSocket."""
        pass

    async def enable_user_active_state(self):
        """Abstract method to enable user active state"""
        pass

    async def disable_user_active_state(self):
        """Abstract method to disable user active state"""
        pass
