import json
import logging

import redis
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model

from .base_consumer import BaseConsumer

logger = logging.getLogger("__name__")
User = get_user_model()
redis_instance = redis.StrictRedis(host='localhost', port=6379, db=0)


class ActivityConsumer(BaseConsumer):
    room_group_name: str

    async def join_group(self):
        self.room_group_name = f'room_activity'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

    def data_user(self):
        user_data = {
            'id': str(self.user.id),
            'full_name': self.user.full_name,
        }
        user_data_json = json.dumps(user_data)
        return user_data_json

    async def enable_user_active_state(self):
        user_info = self.data_user()
        await sync_to_async(redis_instance.sadd)(f'online_users', user_info)
        await self.send_online_users()
        logger.info(f"User {self.user.id} added to online users.")

    async def disable_user_active_state(self):
        user_info = self.data_user()
        await sync_to_async(redis_instance.srem)(f'online_users', user_info)
        await self.send_online_users()
        logger.info(f"User {self.user.id} removed from online users.")

    async def receive(self, text_data=None, bytes_data=None):
        pass

    # @database_sync_to_async
    # def get_all_user_status(self, user_ids):
    #     users = User.objects.filter(id__in=user_ids)
    #     return list(users)

    async def send_online_users(self):
        user_ids_bytes = await sync_to_async(redis_instance.smembers)('online_users')
        user_ids = [uid.decode('utf-8') for uid in user_ids_bytes]
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'online_users_message',
                'online_users': user_ids
            }
        )
        logger.info(f"Send users active: {list(user_ids)}")

    async def online_users_message(self, event):
        await self.send(text_data=json.dumps({
            'online_users': event['online_users']
        }))
