import json
from django.core.management.base import BaseCommand
from kafka import KafkaConsumer
from products.models import Stock, StockHistory

# 🎯 [추가 1] 채널 레이어와 비동기 통신을 위한 모듈 임포트
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class Command(BaseCommand):
    help = 'Kafka에서 주식 데이터를 가져옵니다.'

    def handle(self, *args, **options):
        # 🎯 [추가 2] 채널 레이어 객체 가져오기 (while문 밖에서 한 번만 선언)
        channel_layer = get_channel_layer()

        consumer = KafkaConsumer(
            'stock-data', # 구독할 토픽 이름
            bootstrap_servers=['127.0.0.1:9092'],
            auto_offset_reset='earliest', # 처음부터 읽기
            enable_auto_commit=True,
            group_id='django-group-1', # 컨슈머 그룹
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )

        self.stdout.write(self.style.SUCCESS('데이터 수신 대기 중...'))

        for message in consumer:
            data = message.value  # 이미 json.loads가 된 딕셔너리 형태입니다.
            stock_code = "005930"
            current_price = int(data.get("price", 0)) 
            
            # DB에서 현재 저장된 삼성전자의 정보를 가져옵니다.
            try:
                stock_obj = Stock.objects.get(code=stock_code)
                last_price = stock_obj.current_price
            except Stock.DoesNotExist:
                stock_obj = None
                last_price = None

            # ---------------------------------------------------------
            # DB 저장 로직 (승우님 기존 코드 유지)
            if True: # 가격이 변하던말던 
                stock_obj, created = Stock.objects.update_or_create(
                    code=stock_code,
                    defaults={
                        "name": data.get("name"),
                        "current_price": current_price,
                        "change": data.get("change_num"), # 🎯 change_num을 저장!
                    }
                )
                
                StockHistory.objects.create(
                    stock=stock_obj,
                    price=current_price
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"📢 새 종목 등록: {stock_obj.name}"))
                else:
                    self.stdout.write(self.style.SUCCESS(f"🔄 가격 변동 감지! 갱신 완료: {current_price}원"))
            else:
                self.stdout.write(f"😴 가격 변동 없음 ({current_price}원). 기록을 건너뜁니다.")
            # ---------------------------------------------------------

            # 🎯 [추가 3] DB 처리가 끝난 후, 곧바로 웹소켓으로 데이터 쏘기!
            # async_to_sync를 쓰는 이유: 현재 이 파일은 동기(Sync)로 돌아가는데, 
            # Channels는 비동기(Async)라서 호환을 시켜주는 겁니다.
            try:
                async_to_sync(channel_layer.group_send)(
                    "realtime_data",  # consumers.py에서 정의한 그룹 이름
                    {
                        "type": "send_kafka_data",  # consumers.py에 있는 함수 이름
                        "data": data                # 브라우저로 보낼 실제 데이터
                    }
                )
                self.stdout.write(self.style.SUCCESS(f"🚀 웹소켓 전송 완료!"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"웹소켓 전송 에러: {e}"))