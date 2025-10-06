from django.urls import path
from .views import *
from .image_anz import ImageAnalysisView
from .chatbot import ChatbotView

urlpatterns = [
    # TradeStyle endpoints
    path("trade/styles/", TradeStyleCreateListView.as_view(), name="request-list"),
    path("trade/styles/<int:pk>/", TradeStyleDetailView.as_view(), name="request-detail"),

    # TradeStrategy endpoints
    path("trade/strategies/", TradeStrategyCreateListView.as_view(), name="strategy-list"),
    path("trade/strategies/<int:pk>/", TradeStrategyDetailView.as_view(), name="strategy-detail"),
    
    # Image Analysis & chatbot endpoint
    path("image/analysis/", ImageAnalysisView.as_view(), name="image-analysis"),
    path("chatbot/", ChatbotView.as_view(), name="chatbot"),
    
    # TradingResponse endpoint
    path("trade/result/", TradingResponseListView.as_view(), name="response-list"),
    path("trade/result/<int:pk>/", TradingResponseDetailView.as_view(), name="response-detail"),
    
    # chatbot interaction endpoint
    path("chatbot/list/", ChatbotInteractionListView.as_view(), name="chatbot-interactions"),
    
]
