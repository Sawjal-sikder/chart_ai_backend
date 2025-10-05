from django.db import models

# Create your models here.
class TradeStyle(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
class TradeStrategy(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name


class TradingRequest(models.Model):
    file = models.FileField(upload_to='uploads/')
    trading_style = models.CharField(max_length=255)
    trading_strategy = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"TradingRequest {self.id} - {self.trading_style} - {self.trading_strategy}"
    
class TradingResponse(models.Model):
    request = models.ForeignKey(TradingRequest, on_delete=models.CASCADE)
    response_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"TradingResponse {self.id} for Request {self.request.id}"