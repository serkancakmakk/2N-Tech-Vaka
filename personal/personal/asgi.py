"""
ASGI config for personal project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'personal.settings')
import personal_track.routing
application = get_asgi_application()
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from django.urls import path
from personal_track.consumers import NotificationConsumer
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from personal_track.routing import websocket_urlpatterns

# asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from personal_track.consumers import NotificationConsumer
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'personal.settings')
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter({
            # WebSocket URL'leri burada tanımlanır
            path("ws/notifications/", NotificationConsumer.as_asgi()),
        })
    ),
})