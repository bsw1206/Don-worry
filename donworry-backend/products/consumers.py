import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ProductConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # 'realtime_data'라는 그룹에 참여
        await self.channel_layer.group_add("realtime_data", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("realtime_data", self.channel_name)

    # 🎯 Kafka 데이터가 이 함수를 타고 브라우저로 전송될 겁니다.
    async def send_kafka_data(self, event):
        data = event['data']
        await self.send(text_data=json.dumps(data))