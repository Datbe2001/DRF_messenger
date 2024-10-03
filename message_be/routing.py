from django.urls import re_path
from message_be.apps.message.websocket import chat_consumer

websocket_urlpatterns = [
    re_path(r'ws/chat/$', chat_consumer.ChatConsumer.as_asgi()),
]
