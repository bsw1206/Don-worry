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
from django.urls import path, include, re_path # re_path 추가
from django.views.generic import TemplateView

urlpatterns = [
    # 1. 메인 페이지: Vue의 index.html을 보여줍니다.
    # 기존 path('', views.index)를 아래로 대체합니다.
    path('', TemplateView.as_view(template_name='index.html')), 

    # 2. 관리자 페이지
    path('admin/', admin.site.urls),

    # 3. API 경로: 기존대로 유지
    path('api/products/', include('products.urls')),

    # 4. [중요] Vue Router를 위한 Catch-all 설정 (선택 사항)
    # 사용자가 /login, /survey 같은 주소로 직접 접속했을 때 Django가 404를 내지 않고 
    # Vue가 처리할 수 있게 모든 요청을 index.html로 밀어줍니다.
    # re_path(r'^.*$', TemplateView.as_view(template_name='index.html')),
]


