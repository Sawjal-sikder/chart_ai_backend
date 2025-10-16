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
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.file:
            # Ensure only relative URL (starts with /media/)
            representation['file'] = instance.file.url.replace(self.context['request'].build_absolute_uri('/'), '/')
        else:
            representation['file'] = None
        return representation

class TradingResponseSerializer(serializers.ModelSerializer):
    request_data = TradingRequestSerializer(source='request', read_only=True)
    class Meta:
        model = TradingResponse
        fields = ['id', 'request_data', 'response_data']
        read_only_fields = ['id']



class ChatbotInteractionSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    class Meta:
        model = ChatbotInteraction
        fields = ['id', 'user', 'user_input', 'bot_response', 'created_at']  
        read_only_fields = ['id', 'created_at']

    def get_user(self, obj):
        return obj.user.full_name if obj.user else 'Anonymous'