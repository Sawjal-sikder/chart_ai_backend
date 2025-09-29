from rest_framework import serializers
from .models import Plan, Subscription

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = "__all__"
        read_only_fields = ("stripe_price_id","stripe_product_id")
        
    def get_price_display(self, obj):
        return f"${obj.amount / 100:.2f} per {obj.interval_count} {obj.get_interval_display()}{'s' if obj.interval_count > 1 else ''}"
        
class PlanUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ["name", "interval","interval_count", "amount", "description", "active"]

class SubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer(read_only=True)

    class Meta:
        model = Subscription
        fields = "__all__"
        read_only_fields = (
            "user",
            "stripe_customer_id",
            "stripe_subscription_id",
            "status",
            "trial_end",
            "current_period_end",
            "created_at",
            "updated_at",
        )
