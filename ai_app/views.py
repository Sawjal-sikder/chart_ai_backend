from payment.paymentPermission import HasActiveSubscription
from rest_framework.response import Response
from rest_framework import generics
from .serializers import *
from .models import *

# TradeStyle Views
class TradeStyleCreateListView(generics.ListCreateAPIView):
    queryset = TradeStyle.objects.all()
    serializer_class = TradeStyleSerializer


class TradeStyleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TradeStyle.objects.all()
    serializer_class = TradeStyleSerializer
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "TradeStyle deleted successfully"}, status=204)
        
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"message": "TradeStyle updated successfully", "data": serializer.data})

# TradeStrategy Views
class TradeStrategyCreateListView(generics.ListCreateAPIView):
    queryset = TradeStrategy.objects.all()
    serializer_class = TradeStrategySerializer

class TradeStrategyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TradeStrategy.objects.all()
    serializer_class = TradeStrategySerializer
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "TradeStrategy deleted successfully"}, status=204)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"message": "TradeStrategy updated successfully", "data": serializer.data})

# TradingResponse View
class TradingResponseListView(generics.ListAPIView):
    serializer_class = TradingResponseSerializer
    permission_classes = [HasActiveSubscription]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return TradingResponse.objects.filter(user=user).order_by('-created_at')
        return TradingResponse.objects.none()

class TradingResponseDetailView(generics.RetrieveDestroyAPIView):
    queryset = TradingResponse.objects.all()
    serializer_class = TradingResponseSerializer
    permission_classes = [HasActiveSubscription]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "TradingResponse deleted successfully"}, status=204)
    
    
# Note: ChatbotView has been moved to chatbot.py for better organization.
class ChatbotInteractionListView(generics.ListAPIView):
    serializer_class = ChatbotInteractionSerializer
    permission_classes = [HasActiveSubscription]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return ChatbotInteraction.objects.filter(user=user).order_by('-created_at')
        return ChatbotInteraction.objects.none()