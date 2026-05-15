# products/serializers.py
from rest_framework import serializers
from .models import Product, ProductOption

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOption
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)
    bank_name = serializers.CharField(source='company.kor_co_nm', read_only=True)

    class Meta:
        model = Product
        # 🚨 [여기 확인!] Vue에서 쓰려는 필드들을 모두 여기에 적어줘야 합니다.
        fields = [
            'fin_prdt_cd', 
            'bank_name', 
            'fin_prdt_nm', 
            'options', 
            'join_way',   # 추가
            'spcl_cnd',   # 추가
        ]

