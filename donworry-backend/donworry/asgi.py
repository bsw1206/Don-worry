"""
ASGI config for donworry project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import products.routing # 나중에 만들 파일

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'donworry.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(), # 일반 HTTP 요청
    "websocket": AuthMiddlewareStack( # 웹소켓 요청
        URLRouter(
            products.routing.websocket_urlpatterns
        )
    ),
})
