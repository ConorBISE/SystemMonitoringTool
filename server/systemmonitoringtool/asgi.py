"""
ASGI config for systemmonitoringtool project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.systemmonitoringtool.settings")

django_asgi_application = get_asgi_application()

from server.coreapp.routing import websocket_urlpatterns

application = ProtocolTypeRouter(
    {"http": django_asgi_application, "websocket": URLRouter(websocket_urlpatterns)}
)
