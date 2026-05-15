from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # ws://주소:8000/ws/products/ 경로로 접속 허용
    re_path(r'ws/products/$', consumers.ProductConsumer.as_asgi()),
]