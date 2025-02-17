"""
ASGI config for chat_application project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from master.consumers import *


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_application.settings')

ws_patterns = [
    path('ws/chat/<room_code>', ChatConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket' : URLRouter(ws_patterns)
})
    