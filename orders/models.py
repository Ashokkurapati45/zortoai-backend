# orders/models.py
from django.db import models
from merchants.models import Merchant

class Order(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("VERIFIED", "Verified"),
        ("REJECTED", "Rejected"),
        ("RTO", "Returned"),
        ("DELIVERED", "Delivered"),
    ]

    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name="orders")
    order_id = models.CharField(max_length=128)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pincode = models.CharField(max_length=12, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.order_id} - {self.merchant}"
