from django.db import models
from merchants.models import Merchant

class Order(models.Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=128)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"{self.order_id} - {self.merchant}"
