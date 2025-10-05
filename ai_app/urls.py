from django.urls import path
from .views import *
from .image_anz import ImageAnalysisView

urlpatterns = [
    # TradeStyle endpoints
    path("trade/styles/", TradeStyleCreateListView.as_view(), name="request-list"),
    path("trade/styles/<int:pk>/", TradeStyleDetailView.as_view(), name="request-detail"),

    # TradeStrategy endpoints
    path("trade/strategies/", TradeStrategyCreateListView.as_view(), name="strategy-list"),
    path("trade/strategies/<int:pk>/", TradeStrategyDetailView.as_view(), name="strategy-detail"),
    
    # Image Analysis endpoint
    path("image/analysis/", ImageAnalysisView, name="image-analysis"),
]
