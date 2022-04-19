"""
ASGI config for KvantWorkspace project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

from ChatApp import routing as chat_routing
from NotificationApp import routing as notification_routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Config.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat_routing.websocket_urlpatterns +\
            notification_routing.websocket_urlpatterns
        )
    ),
})
