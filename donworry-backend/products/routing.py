from django.urls import path
from . import consumers

websocket_urlpatterns = [
    # ws://localhost:8000/ws/products/ 연결 처리
    path('ws/products/', consumers.ProductConsumer.as_asgi()),
]