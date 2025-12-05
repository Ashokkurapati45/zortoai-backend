from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Merchant(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="merchants")
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.name
