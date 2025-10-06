from django.contrib import admin
from .models import TradeStyle, TradeStrategy, TradingRequest, TradingResponse


@admin.register(TradeStyle)
class TradeStyleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)
    list_per_page = 20


@admin.register(TradeStrategy)
class TradeStrategyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)
    list_per_page = 20


@admin.register(TradingRequest)
class TradingRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'trading_style', 'trading_strategy', 'created_at')
    search_fields = ('trading_style', 'trading_strategy', 'user__username')
    list_filter = ('trading_style', 'trading_strategy', 'created_at')
    readonly_fields = ('created_at',)
    list_per_page = 20


@admin.register(TradingResponse)
class TradingResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'request', 'created_at')
    search_fields = ('user__username', 'request__trading_style', 'request__trading_strategy')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)
    list_per_page = 20
