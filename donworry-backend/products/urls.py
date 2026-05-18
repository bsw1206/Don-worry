from django.contrib import admin
from django.urls import path, include
from products import views

# products/urls.py
# products/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # GET /api/v1/products/stocks/ -> 전체 상품 목록 조회 (Vue 요청 매칭)
    path('stocks/', views.ProductListView.as_view(), name='product_list'),
    
    # GET /api/v1/products/save/ -> 금감원 데이터 수집 및 저장
    path('save/', views.save_financial_products, name='save_products'), 
    
    # GET /api/v1/products/stock-chart-data/ -> 차트 데이터 조회
    path('stock-chart-data/', views.stock_chart_data, name='stock_chart_data'),  

    # 한국투자증권 뉴스 API 라우팅 엔드포인트 연동
    path('etf/news/', views.get_etf_news, name='etf_news'),

     # GET /api/v1/products/<상품코드>/ -> 특정 상품 상세 조회 (맨 아래 배치)
    path('<str:fin_prdt_cd>/', views.ProductDetailView.as_view(), name='product_detail'),

]