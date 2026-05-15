# apps/management/commands/produce_stock.py
import json
import time
from django.core.management.base import BaseCommand
from kafka import KafkaProducer
import requests
import os
from dotenv import load_dotenv
from requests.exceptions import RequestException

load_dotenv()

def get_access_token():
    app_key = os.getenv("KIS_MOCK_APP_KEY")
    app_secret = os.getenv("KIS_MOCK_APP_SECRET")
    
    print(f"🔑 앱 키 확인: {str(app_key)[:5]}***") 
    print(f"🔑 시크릿 키 확인: {str(app_secret)[:5]}***")
    
    url = "https://openapivts.koreainvestment.com:29443/oauth2/tokenP"
    headers = {"content-type": "application/json"}
    body = {
        "grant_type": "client_credentials",
        "appkey": app_key,
        "appsecret": app_secret
    }
    
    res = requests.post(url, headers=headers, data=json.dumps(body))
    return res.json().get('access_token')

class Command(BaseCommand):
    help = '한국투자증권 API 데이터를 Kafka로 전송합니다.'

    def handle(self, *args, **options):
        # 1. 초기 토큰 발급
        token = get_access_token()
        
        producer = KafkaProducer(
            bootstrap_servers=['127.0.0.1:9092'],
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

        url = "https://openapivts.koreainvestment.com:29443/uapi/domestic-stock/v1/quotations/inquire-price"
        headers = {
            "Content-Type": "application/json",
            "authorization": f"Bearer {token}",
            "appkey": os.getenv("KIS_MOCK_APP_KEY"),
            "appsecret": os.getenv("KIS_MOCK_APP_SECRET"),
            "tr_id": "FHKST01010100"
        }
        params = {"fid_cond_mrkt_div_code": "J", "fid_input_iscd": "005930"}

        self.stdout.write(self.style.SUCCESS('삼성전자 데이터 수집 시작...'))

        try:
            while True:
                try:
                    res = requests.get(url, headers=headers, params=params)
                    data = res.json()
                    
                    if 'output' in data and data['output']:
                        output = data['output']
                        
                        # 🎯 [수정 1] 한투 API 부호(1,2=상승 / 4,5=하락)를 Vue 규격에 맞춤
                        sign = output.get('prdy_vrss_sign')
                        if sign in ['1', '2']:
                            change_status = 'RISE'
                        elif sign in ['4', '5']:
                            change_status = 'FALL'
                        else:
                            change_status = 'EVEN'

                        stock_info = {
                            "name": "삼성전자",
                            "price": output.get('stck_prpr'),
                            "change_num": output.get('prdy_vrss'), # 🎯 DB 저장용 (숫자 형태 문자열)
                            "change_status": change_status,       # 🎯 Vue 화면용 ('RISE', 'FALL')
                            "timestamp": time.time()
                        }
                        producer.send('stock-data', value=stock_info)
                        self.stdout.write(f"✅ 정상 전송: {stock_info['price']}원 ({change_status})")
                        
                    else:
                        error_msg = data.get('msg1', '알 수 없는 에러')
                        self.stdout.write(self.style.WARNING(f"⚠️ API 에러: {error_msg}"))
                        
                        # 🎯 [수정 2] 토큰 만료 에러일 경우 즉시 재발급
                        if "토큰" in error_msg or "인증" in error_msg or "유효하지 않은" in error_msg:
                            self.stdout.write(self.style.WARNING("🔄 토큰 만료 감지! 재발급을 시도합니다..."))
                            token = get_access_token()
                            headers["authorization"] = f"Bearer {token}"
                            self.stdout.write(self.style.SUCCESS("🔑 토큰 재발급 완료!"))

                    time.sleep(3) 

                except RequestException as e:
                    self.stdout.write(self.style.ERROR(f"🚨 네트워크 오류 발생 (5초 후 재시도): {e}"))
                    time.sleep(5)
                    continue

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"에러 발생: {e}"))