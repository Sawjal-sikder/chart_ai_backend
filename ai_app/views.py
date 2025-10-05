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
    queryset = TradingResponse.objects.all()
    serializer_class = TradingResponseSerializer