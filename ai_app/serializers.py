from .models import *
from rest_framework import serializers



class TradeStyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeStyle
        fields = '__all__'
        
class TradeStrategySerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeStrategy
        fields = '__all__'
