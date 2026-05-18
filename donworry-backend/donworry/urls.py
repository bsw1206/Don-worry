"""
URL configuration for donworry project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    # 1. 빌드된 Vue 정적 파일 서빙 (필요 시)
    path('', TemplateView.as_view(template_name='index.html')), 
    
    # 2. 관리자 페이지
    path('admin/', admin.site.urls),

    # 3. API 버전 관리를 적용한 통합 경로
    path('api/v1/products/', include('products.urls')),
]

