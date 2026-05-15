# products/views.py

import requests
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse

# DRF (Django REST Framework)
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Models & Serializers
from .models import FinancialCompany, Product, ProductOption, Stock, StockHistory
from .serializers import ProductSerializer


# ==========================================
# 1. 외부 API 연동 뷰 (금융감독원 데이터 저장)
# ==========================================
@api_view(['GET'])
def save_deposit_products(request):
    finlife_api_key = settings.API_KEYS.get('FINLIFE_API_KEY')
    url = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={finlife_api_key}&topFinGrpNo=020000&pageNo=1'
    
    try:
        response = requests.get(url).json()
        
        # 1. 금융회사 저장
        for co in response.get('result', {}).get('baseList', []):
            FinancialCompany.objects.get_or_create(
                fin_co_no=co['fin_co_no'],
                defaults={'kor_co_nm': co['kor_co_nm']}
            )
            
            # 2. 상품 저장
            Product.objects.get_or_create(
                fin_prdt_cd=co['fin_prdt_cd'],
                defaults={
                    'company_id': co['fin_co_no'],
                    'fin_prdt_nm': co['fin_prdt_nm'],
                    'join_way': co['join_way'],
                    'spcl_cnd': co['spcl_cnd']
                }
            )
            
        # 3. 옵션 저장
        for opt in response.get('result', {}).get('optionList', []):
            try:
                product = Product.objects.get(fin_prdt_cd=opt['fin_prdt_cd'])
                ProductOption.objects.get_or_create(
                    product=product,
                    save_trm=opt['save_trm'],
                    defaults={
                        'intr_rate': opt.get('intr_rate'),
                        'intr_rate2': opt.get('intr_rate2')
                    }
                )
            except Product.DoesNotExist:
                continue

        return Response({"message": "저장 완료"})
    
    except Exception as e:
        return Response({"error": f"데이터 저장 중 에러 발생: {str(e)}"}, status=500)


# ==========================================
# 2. 적금 상품 관련 뷰 (REST API)
# ==========================================
class ProductListView(generics.ListAPIView):
    """전체 상품 목록 조회 API"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailView(generics.RetrieveAPIView):
    """개별 상품 상세 조회 API"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'fin_prdt_cd'


# ==========================================
# 3. 주식 및 화면 렌더링 관련 뷰
# ==========================================
def index(request):
    """메인 페이지 (HTML)"""
    # filter().first()를 쓰면 데이터가 없을 때 알아서 None을 반환합니다.
    samsung_stock = Stock.objects.filter(code='005930').first()
    context = {'samsung_stock': samsung_stock}
    return render(request, 'products/index.html', context)

def product_list(request):
    """상품 목록 페이지 (HTML)"""
    samsung_stock = Stock.objects.filter(code='005930').first()
    context = {'samsung_stock': samsung_stock}
    return render(request, 'products/product_list.html', context)

def stock_chart_data(request):
    """주식 차트용 실시간 데이터 반환 API"""
    histories = StockHistory.objects.filter(stock__code='005930').order_by('-created_at')[:20]
    data = {
        "labels": [h.created_at.strftime('%H:%M:%S') for h in reversed(histories)],
        "prices": [h.price for h in reversed(histories)],
    }
    return JsonResponse(data)