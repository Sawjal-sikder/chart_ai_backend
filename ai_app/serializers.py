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


class TradingRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradingRequest
        fields = ['file', 'trading_style', 'trading_strategy']

class TradingResponseSerializer(serializers.ModelSerializer):
    request_data = TradingRequestSerializer(source='request', read_only=True)
    class Meta:
        model = TradingResponse
        fields = ['id', 'request_data', 'response_data']
        read_only_fields = ['id']
