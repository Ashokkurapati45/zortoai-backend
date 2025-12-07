# orders/serializers.py
from rest_framework import serializers
from .models import Order

class OrderIngestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        # merchant is set from API key, so not in input
        fields = ["id", "order_id", "amount", "pincode", "status", "created_at"]
        read_only_fields = ["id", "status", "created_at"]
